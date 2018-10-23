Co to jest wysoka roznica:


1. Top 10 najwiekszych roznic nominalnych
 / Jakub
2. 10-15% najwiekszych roznic procentowych / Mateusz
3. Liczba wnioskow powyzej mediany
 / Liliana
4. zbadaæ skrajne warto¶ci 5% / Micha³ 



Analiza:

1.rozklad czasu

2.wplyw partnera

3.wplyw kod kraju

4.wplyw klient biznesowy

5.wplyw liczba pasazerow


1.1.

-- Sprawdzenie 50 najwy¿szych róznic pomiêdzy kwotami wnioskowanymi, a wyp³aconymi. 

select id, abs(kwota_rekompensaty - kwota_rekompensaty_oryginalna) as roznica
from wnioski
order by roznica desc
limit 50;

-- Kwota ró¿nic w przedziale od 3.000,00 do 600,00 euro.

1.2.

-- 50 najwiêkszych ró¿nic z pomiêdzy kwotami wnioskowanymi, a wyp³aconymi. Wyniki zosta³y posortowane po partnerach.

with top_roznica as
(
    select id, partner, kod_kraju, abs(kwota_rekompensaty - kwota_rekompensaty_oryginalna) as roznica
from wnioski
order by roznica desc
limit 50
)

select * from top_roznica
order by partner;

-- W wyliczonym zakresie s± po cztery sprawy partnera kiribati i tui. Dla pozosta³ych wniosków nie mamy informacji o partnerze (null).

1.3.

-- 50 najwiêkszych ró¿nic pomiêdzy kwotami wnioskowanymi, a wyp³aconymi. Wyniki zosta³y posortowane po kodzie kraju.

with top_roznica as
(
    select id, partner, kod_kraju, abs(kwota_rekompensaty - kwota_rekompensaty_oryginalna) as roznica
from wnioski
order by roznica desc
limit 50
)
select distinct kod_kraju, count(kod_kraju) over (partition by kod_kraju) as kod
from top_roznica
order by kod desc;

-- Z 50 wniosków z najwy¿sz± ró¿nic±, a¿ 22 sprawy (44%) s± z kodem kraju 'PL', 10 (20%) spraw jest z kodem 'ZZ'. Dla pozosta³ych kodów wniosków nie jest wiêcej, ni¿ 5.

-- Sprawdzenie wszystkich wniosków z ró¿nic± pomiêdzy kwotami wnioskowanymi, a wyp³aconymi.

select distinct kod_kraju,
       count(kod_kraju) over (partition by kod_kraju) as kod
from wnioski
where abs(kwota_rekompensaty - kwota_rekompensaty_oryginalna) > 0
order by kod desc;

-- Najwiêcej jest wniosków z kodem kraju 'ZZ'- 1573, nastêpnie z kodem kraju 'IE' - 371 i 'PL' - 272 (11,66%).











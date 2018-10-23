Co to jest wysoka roznica:


1. Top 10 najwiekszych roznic nominalnych
 / Jakub
2. 10-15% najwiekszych roznic procentowych / Mateusz
3. Liczba wnioskow powyzej mediany
 / Liliana
4. zbada� skrajne warto�ci 5% / Micha� 



Analiza:

1.rozklad czasu

2.wplyw partnera

3.wplyw kod kraju

4.wplyw klient biznesowy

5.wplyw liczba pasazerow


1.1.

-- Sprawdzenie 50 najwy�szych r�znic pomi�dzy kwotami wnioskowanymi, a wyp�aconymi. 

select id, abs(kwota_rekompensaty - kwota_rekompensaty_oryginalna) as roznica
from wnioski
order by roznica desc
limit 50;

-- Kwota r�nic w przedziale od 3.000,00 do 600,00 euro.

1.2.

-- 50 najwi�kszych r�nic z pomi�dzy kwotami wnioskowanymi, a wyp�aconymi. Wyniki zosta�y posortowane po partnerach.

with top_roznica as
(
    select id, partner, kod_kraju, abs(kwota_rekompensaty - kwota_rekompensaty_oryginalna) as roznica
from wnioski
order by roznica desc
limit 50
)

select * from top_roznica
order by partner;

-- W wyliczonym zakresie s� po cztery sprawy partnera kiribati i tui. Dla pozosta�ych wniosk�w nie mamy informacji o partnerze (null).

1.3.

-- 50 najwi�kszych r�nic pomi�dzy kwotami wnioskowanymi, a wyp�aconymi. Wyniki zosta�y posortowane po kodzie kraju.

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

-- Z 50 wniosk�w z najwy�sz� r�nic�, a� 22 sprawy (44%) s� z kodem kraju 'PL', 10 (20%) spraw jest z kodem 'ZZ'. Dla pozosta�ych kod�w wniosk�w nie jest wi�cej, ni� 5.

-- Sprawdzenie wszystkich wniosk�w z r�nic� pomi�dzy kwotami wnioskowanymi, a wyp�aconymi.

select distinct kod_kraju,
       count(kod_kraju) over (partition by kod_kraju) as kod
from wnioski
where abs(kwota_rekompensaty - kwota_rekompensaty_oryginalna) > 0
order by kod desc;

-- Najwi�cej jest wniosk�w z kodem kraju 'ZZ'- 1573, nast�pnie z kodem kraju 'IE' - 371 i 'PL' - 272 (11,66%).











2. 10-15% najwiekszych roznic procentowych / Mateusz

Analiza:
1.rozklad czasu
2.wplyw partnera
3.wplyw kod kraju
4.wplyw klient biznesowy
5.wplyw liczba pasazerow

---liczba wnioskow wyplaconych
select count(1) as liczba_wnioskow,sum(liczba_pasazerow) as liczba_pasazerow from wnioski
where lower(stan_wniosku) like 'wypl%'

-----2. roznice procentowe powyzej 100%
select count(id)
from wnioski
where lower(stan_wniosku) not like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
--and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100

-- Tabela prezentuje roznice nominalne i roznice procentowe dla wnioskow tylko wyplaconych
-- i dla tych ktorych roznica pomiedzy kwota wnioskowana a wyplacona jest wieksza niz 100%

-----------Analiza: 2.1.rozklad czasu
with czas as (select to_char(data_utworzenia,'YYYY') as rokmsc,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
--and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 5 desc)

select rokmsc,sum(wyplacone),max(wyplacone),count(1) from czas
group by rokmsc
order by 4 desc

-----------Analiza: 2.2.wplyw partnera
with partnerzy as (
  select partner,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
--and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 5 desc
)
select partner, max(roznica),sum(roznica)
from partnerzy
group by partner

-----------Analiza: 2.3.wplyw kod kraju
with partnerzy as (
  select id,partner,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
--and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 5 desc
)
select kod_kraju,sum(roznica)
from partnerzy p
join wnioski w on p.id = w.id
group by kod_kraju
order by 2 desc

-----------Analiza: 2.4.wplyw klient
with partnerzy as (
  select id,partner,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
--and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 5 desc
)
select typ_podrozy,sum(roznica)
from partnerzy p
join wnioski w on p.id = w.id
group by typ_podrozy
order by 2 desc

--- nie ma wpływu

----------Zapytanie Podsumowanie Wniosków

with partnerzy as (
  select id,partner,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
--and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 5 desc
),
wnioski_nasze as (select w.id,w.kod_kraju,w.opoznienie,
                         sum(roznica) as suma_roznica1,max(roznica) as max_roznica2,count(w.id) as liczba
from partnerzy p
join wnioski w on p.id = w.id
where kod_kraju in ('ZZ') --and typ_podrozy is null
     --and to_char(data_utworzenia,'YYYY-MM') > '2017-06'
     and opoznienie like '%> 3h%'
group by w.id,w.kod_kraju,w.opoznienie
order by 1 desc)

select wn.kod_kraju,wn.opoznienie,count(1),kod_wyjazdu,kod_przyjazdu
from wnioski_nasze wn
join podroze p2 on wn.id = p2.id_wniosku
join szczegoly_podrozy sp on p2.id = sp.id_podrozy
group by wn.kod_kraju,wn.opoznienie,kod_wyjazdu,kod_przyjazdu

---- Komentarz: Najwiecej róznic wystepuje w lotach pomiedzy lotniskami HHN-FRA,
---- okazuje sie ze obydwa lotniska znajduja sie w Niemczech najprawdopodniej blad w bazie,


-----Potwierdzenie wniosków

with wnioski_spr as (select w.id
from wnioski w
join podroze p on w.id = p.id_wniosku
join szczegoly_podrozy s2 on p.id = s2.id_podrozy
where kod_wyjazdu = 'HHN' and kod_przyjazdu = 'FRA' and stan_wniosku like 'wypl%'
group by w.id)
select w.id,count(1)
from wnioski_spr w
join podroze p on w.id = p.id_wniosku
join szczegoly_podrozy s2 on p.id = s2.id_podrozy
group by w.id
order by 2 desc
;
select w.id,s2.kod_wyjazdu,s2.kod_przyjazdu,s2.data_wyjazdu,s2.data_utworzenia,s2.data_aktualizacji
from wnioski w
join podroze p on w.id = p.id_wniosku
join szczegoly_podrozy s2 on p.id = s2.id_podrozy
where w.id=2048230



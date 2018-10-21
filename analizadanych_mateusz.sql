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
select id,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 2 desc
-- Tabela prezentuje roznice nominalne i roznice procentowe dla wnioskow tylko wyplaconych
-- i dla tych ktorych roznica pomiedzy kwota wnioskowana a wyplacona jest wieksza niz 100%

-----------Analiza: 2.1.rozklad czasu
with czas as (select to_char(data_utworzenia,'YYYY-MM') as rokmsc,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 5 desc)

select rokmsc,sum(wyplacone),max(wyplacone),count(1) from czas
group by rokmsc
order by rokmsc

-----------Analiza: 2.2.wplyw partnera
select partner,kwota_rekompensaty as wyplacone,kwota_rekompensaty_oryginalna,
       abs(kwota_rekompensaty_oryginalna-kwota_rekompensaty) as roznica,
       100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty as procent
from wnioski
where lower(stan_wniosku) like 'wypl%'
and kwota_rekompensaty - kwota_rekompensaty_oryginalna <> 0
and kwota_rekompensaty <> 0
and 100.0*(kwota_rekompensaty_oryginalna-kwota_rekompensaty)/kwota_rekompensaty > 100
order by 5 desc


-----------Analiza: 2.3.wplyw kod kraju

-----------Analiza: 2.4.wplyw klient biznesowy

-----------Analiza: 2.5.wplyw liczba pasazerow
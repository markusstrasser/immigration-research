### A0. Pre-period coefficients of the headline specifications

Log points x 100 (SE), 2018 = 0; per 10 points of the share or per log point of arrests. QCEW starts in 2014 and CDTFA in 2015. Every other specification's pre-period coefficients are in the `derived/*_coefs.csv` files.

| specification | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 |
|---|---|---|---|---|---|---|
| (a) QCEW 7225 employment, P1, unweighted |  |  | -1.8 (1.2) | -1.9 (0.9) | -1.2 (0.9) | -0.3 (0.6) |
| (a) CBP full-service employment, P2, unweighted | -5.0 (2.2) | -3.3 (2.0) | -1.8 (2.0) | -0.8 (1.8) | -1.2 (1.7) | +1.3 (1.1) |
| (a2) full-service establishments, Hispanic share, unweighted | +0.5 (1.3) | +0.9 (1.4) | +1.2 (1.3) | +0.2 (1.4) | -0.6 (1.0) | +0.2 (0.8) |
| (a2) limited-service employment, Hispanic share, pop-weighted | -0.4 (0.7) | -0.8 (0.7) | -1.8 (0.8) | -1.2 (0.7) | -0.5 (0.5) | -0.2 (0.4) |
| (b) LA ZIPs full-service, Hispanic share | -1.6 (0.7) | -1.5 (0.6) | -1.5 (0.6) | -1.6 (0.5) | -0.9 (0.5) | -0.7 (0.3) |
| (b) LA ZIPs limited-service, Hispanic share | +0.8 (0.6) | +1.4 (0.6) | +0.7 (0.6) | +0.7 (0.4) | +0.5 (0.4) | +0.3 (0.2) |
| (b) City ZIPs full-service, arrests | -3.4 (2.2) | -3.0 (2.1) | -4.2 (2.3) | -3.1 (1.3) | -2.8 (1.2) | -1.4 (0.7) |
| (b) City ZIPs full-service, arrests, Poisson | -2.3 (1.6) | -2.8 (1.3) | -3.1 (1.2) | -2.5 (1.1) | -1.5 (0.7) | -0.9 (0.4) |
| sales: LA County cities C08, unweighted |  |  |  | -0.4 (0.3) | -0.3 (0.2) | -0.2 (0.1) |
| sales: counties C08, pop-weighted |  |  |  | -0.6 (0.3) | -0.4 (0.2) | -0.1 (0.1) |



### A1. California against other states' counties (design a), every specification

Log points x 100 (about percent). b2019 is the 2019 coefficient with its county-clustered SE; b2022-23 the mean of 2022 and 2023; pre p the joint test of 2012-2017 (QCEW 2014-2017); perm p the placebo-state rank p-value (P1 only).

| source | NAICS | outcome | pool | weight | CA/controls | b2019 (SE) | b2020-21 | b2022-23 | pre p | perm p 2019 | perm p 2022-23 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cbp | 722511 | estab | P1 | none | 57/581 | -0.1 (1.0) | -1.2 | -2.9 | 0.84 |  |  |
| cbp | 722511 | estab | P1 | pop | 57/581 | -0.2 (0.4) | -2.5 | -5.1 | 0.00 |  |  |
| cbp | 722511 | estab | P2 | none | 57/180 | -0.5 (1.1) | -2.0 | -4.7 | 0.65 |  |  |
| cbp | 722511 | estab | P2 | pop | 57/180 | -0.5 (0.5) | -3.2 | -6.0 | 0.00 |  |  |
| cbp | 722511 | emp | P1 | none | 54/516 | -1.8 (1.0) | -9.7 | -3.3 | 0.00 | 0.48 | 0.64 |
| cbp | 722511 | emp | P1 | pop | 54/516 | -1.2 (0.5) | -7.9 | -3.8 | 0.00 | 0.64 | 0.48 |
| cbp | 722511 | emp | P2 | none | 54/178 | -2.4 (1.1) | -9.0 | -3.5 | 0.07 |  |  |
| cbp | 722511 | emp | P2 | pop | 54/178 | -2.0 (0.5) | -9.9 | -5.1 | 0.00 |  |  |
| cbp | 722511 | payann | P1 | none | 56/557 | +1.6 (0.8) | -9.4 | +0.4 | 0.00 |  |  |
| cbp | 722511 | payann | P1 | pop | 56/557 | +1.1 (0.4) | -7.3 | -1.9 | 0.00 |  |  |
| cbp | 722511 | payann | P2 | none | 56/180 | +1.1 (0.8) | -6.8 | +0.4 | 0.00 |  |  |
| cbp | 722511 | payann | P2 | pop | 56/180 | +0.9 (0.5) | -8.7 | -2.7 | 0.00 |  |  |
| cbp | 722513 | estab | P1 | none | 55/569 | -0.5 (0.8) | -2.7 | -0.4 | 0.31 |  |  |
| cbp | 722513 | estab | P1 | pop | 55/569 | -1.0 (0.4) | -2.4 | -0.9 | 0.00 |  |  |
| cbp | 722513 | estab | P2 | none | 55/179 | -0.4 (0.9) | -2.5 | -0.6 | 0.56 |  |  |
| cbp | 722513 | estab | P2 | pop | 55/179 | -1.3 (0.5) | -3.3 | -2.0 | 0.00 |  |  |
| cbp | 722513 | emp | P1 | none | 53/517 | +0.7 (0.9) | -4.1 | -2.3 | 0.69 | 0.88 | 0.84 |
| cbp | 722513 | emp | P1 | pop | 53/517 | +0.0 (0.6) | -2.9 | -1.2 | 0.05 | 1.00 | 0.72 |
| cbp | 722513 | emp | P2 | none | 53/174 | +1.6 (1.1) | -3.2 | -2.8 | 0.49 |  |  |
| cbp | 722513 | emp | P2 | pop | 53/174 | -0.4 (0.7) | -3.6 | -2.6 | 0.00 |  |  |
| cbp | 722513 | payann | P1 | none | 54/540 | +2.8 (0.9) | -0.9 | +1.2 | 0.00 |  |  |
| cbp | 722513 | payann | P1 | pop | 54/540 | +2.2 (0.7) | +1.0 | +0.8 | 0.00 |  |  |
| cbp | 722513 | payann | P2 | none | 54/178 | +3.1 (1.1) | +0.2 | -1.3 | 0.01 |  |  |
| cbp | 722513 | payann | P2 | pop | 54/178 | +2.7 (1.0) | +0.6 | -0.4 | 0.00 |  |  |
| cbp | 722330 | estab | P1 | none | 27/119 | -2.5 (4.0) | -3.7 | -4.1 | 0.53 | 0.93 | 0.87 |
| cbp | 722330 | estab | P1 | pop | 27/119 | -6.0 (3.0) | -11.4 | -11.8 | 0.15 | 0.53 | 0.67 |
| cbp | 722330 | estab | P2 | none | 27/53 | -8.0 (5.7) | -10.7 | -14.0 | 0.99 |  |  |
| cbp | 722330 | estab | P2 | pop | 27/53 | -8.5 (3.6) | -17.5 | -19.6 | 0.95 |  |  |
| cbp | 722330 | emp | P1 | none | 10/15 | +1.1 (12.3) | -10.4 | -7.8 | 0.02 |  |  |
| cbp | 722330 | emp | P1 | pop | 10/15 | -7.5 (8.5) | -19.4 | -14.4 | 0.00 |  |  |
| cbp | 722330 | emp | P2 | none | 10/7 | -1.2 (10.5) | +4.8 | +17.0 | 0.01 |  |  |
| cbp | 722330 | emp | P2 | pop | 10/7 | -9.2 (7.8) | -14.8 | -5.2 | 0.00 |  |  |
| cbp | 722330 | payann | P1 | none | 16/62 | -4.1 (8.0) | -20.2 | -24.4 | 0.00 |  |  |
| cbp | 722330 | payann | P1 | pop | 16/62 | -6.0 (4.9) | -23.2 | -20.0 | 0.00 |  |  |
| cbp | 722330 | payann | P2 | none | 16/29 | +4.7 (8.4) | -2.5 | -6.9 | 0.02 |  |  |
| cbp | 722330 | payann | P2 | pop | 16/29 | -3.3 (6.5) | -17.4 | -11.8 | 0.00 |  |  |
| cbp | 445110 | estab | P1 | none | 56/448 | +1.2 (1.7) | +3.9 | +6.6 | 0.01 |  |  |
| cbp | 445110 | estab | P1 | pop | 56/448 | +1.4 (0.7) | +3.3 | +3.4 | 0.02 |  |  |
| cbp | 445110 | estab | P2 | none | 56/159 | +0.9 (1.9) | +3.7 | +6.6 | 0.01 |  |  |
| cbp | 445110 | estab | P2 | pop | 56/159 | +1.4 (0.9) | +2.6 | +2.3 | 0.06 |  |  |
| cbp | 445110 | emp | P1 | none | 53/281 | -1.4 (1.7) | +0.2 | -0.5 | 0.00 | 0.88 | 0.96 |
| cbp | 445110 | emp | P1 | pop | 53/281 | -0.2 (0.6) | -1.4 | -3.5 | 0.00 | 0.96 | 0.71 |
| cbp | 445110 | emp | P2 | none | 53/103 | -2.3 (1.7) | +0.0 | +0.2 | 0.01 |  |  |
| cbp | 445110 | emp | P2 | pop | 53/103 | -1.3 (0.7) | -1.3 | -3.8 | 0.00 |  |  |
| cbp | 445110 | payann | P1 | none | 53/295 | +3.2 (1.5) | +7.5 | +2.4 | 0.03 |  |  |
| cbp | 445110 | payann | P1 | pop | 53/295 | +1.8 (0.6) | +4.0 | -0.5 | 0.02 |  |  |
| cbp | 445110 | payann | P2 | none | 53/108 | +3.6 (1.5) | +7.7 | +3.8 | 0.00 |  |  |
| cbp | 445110 | payann | P2 | pop | 53/108 | +1.6 (0.9) | +3.8 | +0.1 | 0.03 |  |  |
| cbp | 7225 | emp | P1 | none | 56/572 | -1.4 (0.7) | -6.4 | -3.3 | 0.12 | 0.60 | 0.68 |
| cbp | 7225 | emp | P1 | pop | 56/572 | -0.8 (0.4) | -4.1 | -2.3 | 0.01 | 0.48 | 0.60 |
| cbp | 7225 | emp | P2 | none | 56/181 | -1.6 (0.8) | -5.8 | -3.7 | 0.80 |  |  |
| cbp | 7225 | emp | P2 | pop | 56/181 | -1.3 (0.4) | -5.4 | -3.8 | 0.32 |  |  |
| qcew | 7225 | estabs | P1 | none | 51/415 | +0.5 (0.5) | -2.2 | -4.4 | 0.00 |  |  |
| qcew | 7225 | estabs | P1 | pop | 51/415 | +0.5 (0.3) | -1.4 | -2.7 | 0.00 |  |  |
| qcew | 7225 | estabs | P2 | none | 51/147 | +0.2 (0.6) | -2.7 | -4.8 | 0.00 |  |  |
| qcew | 7225 | estabs | P2 | pop | 51/147 | +0.1 (0.4) | -2.3 | -3.7 | 0.00 |  |  |
| qcew | 7225 | emp | P1 | none | 51/415 | -0.4 (0.5) | -7.0 | -3.0 | 0.24 | 0.96 | 0.65 |
| qcew | 7225 | emp | P1 | pop | 51/415 | +0.1 (0.3) | -4.0 | -1.7 | 0.44 | 0.88 | 0.69 |
| qcew | 7225 | emp | P2 | none | 51/147 | -0.3 (0.6) | -5.6 | -4.0 | 0.31 |  |  |
| qcew | 7225 | emp | P2 | pop | 51/147 | -0.1 (0.3) | -6.0 | -3.2 | 0.29 |  |  |
| qcew | 7225 | wages | P1 | none | 51/415 | +0.9 (0.6) | -4.3 | -0.7 | 0.00 |  |  |
| qcew | 7225 | wages | P1 | pop | 51/415 | +1.0 (0.4) | -2.5 | -0.5 | 0.00 |  |  |
| qcew | 7225 | wages | P2 | none | 51/147 | +0.7 (0.7) | -2.7 | -2.0 | 0.00 |  |  |
| qcew | 7225 | wages | P2 | pop | 51/147 | +0.8 (0.5) | -4.1 | -1.5 | 0.00 |  |  |
| qcew | 722511 | emp | P1 | none | 53/399 | +0.2 (0.7) | -11.3 | -4.9 | 0.36 |  |  |
| qcew | 722511 | emp | P1 | pop | 53/399 | -0.3 (0.4) | -9.2 | -4.4 | 0.39 |  |  |
| qcew | 722511 | emp | P2 | none | 53/154 | -0.1 (0.7) | -10.3 | -6.5 | 0.22 |  |  |
| qcew | 722511 | emp | P2 | pop | 53/154 | -0.8 (0.4) | -12.1 | -6.8 | 0.04 |  |  |
| qcew | 722513 | emp | P1 | none | 51/494 | -0.9 (0.8) | -4.2 | -2.6 | 0.00 |  |  |
| qcew | 722513 | emp | P1 | pop | 51/494 | +0.5 (0.3) | -0.9 | +0.2 | 0.04 |  |  |
| qcew | 722513 | emp | P2 | none | 51/165 | -0.1 (0.9) | -2.6 | -2.6 | 0.14 |  |  |
| qcew | 722513 | emp | P2 | pop | 51/165 | +0.5 (0.5) | -2.0 | -0.4 | 0.10 |  |  |
| qcew | 445110 | emp | P1 | none | 43/218 | -0.1 (0.8) | +0.5 | -0.2 | 0.27 |  |  |
| qcew | 445110 | emp | P1 | pop | 43/218 | -0.4 (0.5) | +0.5 | +1.6 | 0.24 |  |  |
| qcew | 445110 | emp | P2 | none | 43/92 | -0.6 (0.8) | +0.1 | +0.4 | 0.51 |  |  |
| qcew | 445110 | emp | P2 | pop | 43/92 | -0.4 (0.6) | -0.6 | +1.1 | 0.27 |  |  |


### A2. Triple difference (design a2), every specification

Per 10 points of the exposure share; state x year fixed effects.

| NAICS | outcome | exposure | weight | CA/other counties | d2019 (SE) | d2020-21 | d2022-23 | pre p |
|---|---|---|---|---|---|---|---|---|
| 722511 | estab | hisp_share | none | 57/2658 | -1.0 (0.6) | +0.2 | +1.2 | 0.33 |
| 722511 | estab | hisp_share | pop | 57/2658 | -0.0 (0.3) | +0.6 | +0.7 | 0.59 |
| 722511 | estab | mexborn_share | none | 57/2658 | -3.2 (1.8) | -0.0 | +2.4 | 0.88 |
| 722511 | estab | mexborn_share | pop | 57/2658 | -0.6 (1.1) | +1.9 | +1.9 | 0.28 |
| 722511 | estab | foodprep_hisp_share | none | 57/2658 | -0.7 (0.5) | -0.2 | +1.0 | 0.21 |
| 722511 | estab | foodprep_hisp_share | pop | 57/2658 | +0.0 (0.3) | +0.3 | +0.3 | 0.38 |
| 722511 | emp | hisp_share | none | 54/2305 | +0.6 (0.6) | +1.1 | +3.0 | 0.10 |
| 722511 | emp | hisp_share | pop | 54/2305 | +0.0 (0.3) | +2.4 | +2.9 | 0.44 |
| 722511 | emp | mexborn_share | none | 54/2305 | +1.8 (2.1) | +1.7 | +7.3 | 0.16 |
| 722511 | emp | mexborn_share | pop | 54/2305 | +1.7 (1.0) | +8.6 | +10.1 | 0.09 |
| 722511 | emp | foodprep_hisp_share | none | 54/2305 | +0.4 (0.7) | +0.7 | +2.3 | 0.65 |
| 722511 | emp | foodprep_hisp_share | pop | 54/2305 | +0.1 (0.3) | +1.8 | +2.1 | 0.63 |
| 722513 | estab | hisp_share | none | 55/2522 | +0.9 (0.5) | +1.0 | +2.3 | 0.66 |
| 722513 | estab | hisp_share | pop | 55/2522 | +0.1 (0.3) | +1.0 | +1.9 | 0.02 |
| 722513 | estab | mexborn_share | none | 55/2522 | +2.2 (1.6) | +3.2 | +5.8 | 0.50 |
| 722513 | estab | mexborn_share | pop | 55/2522 | +0.1 (0.9) | +2.6 | +5.4 | 0.08 |
| 722513 | estab | foodprep_hisp_share | none | 55/2522 | +0.5 (0.5) | +0.3 | +0.9 | 0.58 |
| 722513 | estab | foodprep_hisp_share | pop | 55/2522 | -0.2 (0.3) | +0.5 | +1.3 | 0.02 |
| 722513 | emp | hisp_share | none | 53/2233 | -0.7 (0.6) | -0.6 | +1.1 | 0.15 |
| 722513 | emp | hisp_share | pop | 53/2233 | -0.2 (0.4) | +2.2 | +2.5 | 0.00 |
| 722513 | emp | mexborn_share | none | 53/2233 | -2.3 (1.7) | -2.6 | +1.4 | 0.16 |
| 722513 | emp | mexborn_share | pop | 53/2233 | -2.2 (1.2) | +4.4 | +5.0 | 0.04 |
| 722513 | emp | foodprep_hisp_share | none | 53/2233 | -0.3 (0.5) | -0.9 | +0.2 | 0.07 |
| 722513 | emp | foodprep_hisp_share | pop | 53/2233 | -0.4 (0.4) | +1.7 | +1.8 | 0.00 |
| 722330 | estab | hisp_share | none | 27/273 | +1.8 (2.9) | +5.3 | +6.2 | 0.00 |
| 722330 | estab | hisp_share | pop | 27/273 | +2.6 (2.2) | +7.7 | +10.5 | 0.25 |
| 722330 | estab | mexborn_share | none | 27/273 | +3.9 (10.1) | +15.7 | +16.1 | 0.00 |
| 722330 | estab | mexborn_share | pop | 27/273 | +3.7 (8.6) | +12.6 | +26.4 | 0.02 |
| 722330 | estab | foodprep_hisp_share | none | 27/273 | +2.0 (2.9) | +4.8 | +5.0 | 0.00 |
| 722330 | estab | foodprep_hisp_share | pop | 27/273 | +2.1 (2.1) | +5.4 | +7.1 | 0.58 |
| 722330 | emp | hisp_share | none | 10/20 | -2.1 (14.0) | +1.4 | -11.7 | 0.00 |
| 722330 | emp | hisp_share | pop | 10/20 | +7.9 (15.4) | +10.1 | +9.2 | 0.00 |
| 722330 | emp | mexborn_share | none | 10/20 | -53.6 (39.1) | -104.8 | -87.2 | 0.00 |
| 722330 | emp | mexborn_share | pop | 10/20 | -43.8 (39.6) | -69.5 | -20.4 | 0.00 |
| 722330 | emp | foodprep_hisp_share | none | 10/20 | +8.2 (11.8) | -2.8 | +14.8 | 0.01 |
| 722330 | emp | foodprep_hisp_share | pop | 10/20 | +11.5 (9.3) | +4.2 | +25.0 | 0.00 |
| 445110 | estab | hisp_share | none | 56/1969 | +0.2 (0.8) | +0.3 | +0.5 | 0.17 |
| 445110 | estab | hisp_share | pop | 56/1969 | -0.4 (0.4) | -0.0 | +0.1 | 0.04 |
| 445110 | estab | mexborn_share | none | 56/1969 | +1.6 (2.8) | +1.0 | +0.3 | 0.11 |
| 445110 | estab | mexborn_share | pop | 56/1969 | -1.2 (1.5) | -1.4 | -3.3 | 0.01 |
| 445110 | estab | foodprep_hisp_share | none | 56/1969 | -0.0 (1.1) | -0.6 | -1.0 | 0.13 |
| 445110 | estab | foodprep_hisp_share | pop | 56/1969 | -0.7 (0.4) | -0.6 | -1.2 | 0.02 |
| 445110 | emp | hisp_share | none | 53/1257 | +0.6 (0.9) | -0.2 | +0.9 | 0.08 |
| 445110 | emp | hisp_share | pop | 53/1257 | -0.2 (0.4) | -1.6 | -1.5 | 0.04 |
| 445110 | emp | mexborn_share | none | 53/1257 | +1.7 (2.7) | +1.2 | +4.0 | 0.13 |
| 445110 | emp | mexborn_share | pop | 53/1257 | -0.7 (1.3) | -4.9 | -4.8 | 0.01 |
| 445110 | emp | foodprep_hisp_share | none | 53/1257 | +0.4 (1.1) | -1.8 | -1.4 | 0.16 |
| 445110 | emp | foodprep_hisp_share | pop | 53/1257 | -0.2 (0.4) | -1.8 | -2.2 | 0.00 |


### A3. Triple difference, California against placebo states (Hispanic share)

p10/p90 are the 10th and 90th percentiles of the same coefficient with each other state (20+ counties) in California's place.

| NAICS | outcome | weight | placebo states | CA d2019 | placebo p10-p90 | perm p | CA d2022-23 | placebo p10-p90 | perm p |
|---|---|---|---|---|---|---|---|---|---|
| 445110 | emp | none | 26 | +0.6 | -5.3 to +6.2 | 0.81 | +0.9 | -5.8 to +14.8 | 0.85 |
| 445110 | emp | pop | 26 | -0.2 | -5.0 to +4.5 | 1.00 | -1.5 | -4.2 to +23.6 | 0.74 |
| 722330 | estab | none | 1 | +1.8 | -0.8 to -0.8 | 0.50 | +6.2 | -9.0 to -9.0 | 1.00 |
| 722330 | estab | pop | 1 | +2.6 | +0.2 to +0.2 | 0.50 | +10.5 | -4.0 to -4.0 | 0.50 |
| 722511 | emp | none | 37 | +0.6 | -7.2 to +6.4 | 0.84 | +3.0 | -10.0 to +7.5 | 0.47 |
| 722511 | emp | pop | 37 | +0.0 | -3.3 to +4.6 | 0.97 | +2.9 | -20.8 to +4.2 | 0.47 |
| 722511 | estab | none | 38 | -1.0 | -5.3 to +3.4 | 0.77 | +1.2 | -3.7 to +13.3 | 0.90 |
| 722511 | estab | pop | 38 | -0.0 | -2.5 to +4.8 | 1.00 | +0.7 | -2.0 to +8.0 | 0.79 |
| 722513 | emp | none | 35 | -0.7 | -3.0 to +7.3 | 0.86 | +1.1 | -4.7 to +14.7 | 0.94 |
| 722513 | emp | pop | 35 | -0.2 | -3.9 to +4.8 | 0.86 | +2.5 | -6.8 to +6.4 | 0.42 |
| 722513 | estab | none | 37 | +0.9 | -1.8 to +4.0 | 0.71 | +2.3 | -3.2 to +8.7 | 0.55 |
| 722513 | estab | pop | 37 | +0.1 | -2.0 to +3.1 | 0.92 | +1.9 | -1.6 to +5.5 | 0.39 |


### A4. Los Angeles County ZIPs (design b), every specification

Per 10 points of the share, or per log point of 2010-2016 LAPD vending arrests (City of LA ZIPs). The employment index rows are invalid (size classes suppressed from 2017) and are shown only because they were computed.

| NAICS | exposure | outcome | ZIPs | b2019 (SE) | b2020-21 | b2022-23 | pre p | note |
|---|---|---|---|---|---|---|---|---|
| 722511 | hisp_share | log_estab | 258 | +0.1 (0.3) | +1.2 | +1.4 | 0.05 |  |
| 722511 | hisp_share | estab_poisson | 258 | +0.1 (0.2) | +0.6 | +0.8 | 0.00 |  |
| 722511 | hisp_share | log_emp_index | 258 | +3.0 (1.7) | +5.7 | +6.9 | 0.05 | invalid |
| 722511 | mexborn_share | log_estab | 258 | +0.5 (0.9) | +3.9 | +4.1 | 0.13 |  |
| 722511 | mexborn_share | estab_poisson | 258 | -0.0 (0.7) | +1.8 | +2.1 | 0.00 |  |
| 722511 | mexborn_share | log_emp_index | 258 | +7.7 (4.5) | +16.5 | +19.4 | 0.04 | invalid |
| 722511 | arrests | log_estab | 98 | -0.7 (0.7) | -0.6 | +0.0 | 0.20 |  |
| 722511 | arrests | estab_poisson | 98 | -0.3 (0.6) | -1.0 | -1.0 | 0.07 |  |
| 722511 | arrests | log_emp_index | 98 | +6.2 (4.2) | +0.7 | +2.6 | 0.08 | invalid |
| 722513 | hisp_share | log_estab | 262 | +0.0 (0.2) | +0.9 | +0.5 | 0.11 |  |
| 722513 | hisp_share | estab_poisson | 262 | +0.2 (0.2) | +0.9 | +0.7 | 0.02 |  |
| 722513 | hisp_share | log_emp_index | 262 | -1.6 (1.3) | +1.4 | -0.8 | 0.04 | invalid |
| 722513 | mexborn_share | log_estab | 262 | +0.4 (0.6) | +2.6 | +1.3 | 0.01 |  |
| 722513 | mexborn_share | estab_poisson | 262 | +0.6 (0.5) | +2.4 | +1.4 | 0.00 |  |
| 722513 | mexborn_share | log_emp_index | 262 | -3.8 (3.4) | +3.6 | -1.9 | 0.02 | invalid |
| 722513 | arrests | log_estab | 98 | +0.2 (0.5) | -0.2 | -0.0 | 0.17 |  |
| 722513 | arrests | estab_poisson | 98 | +0.0 (0.4) | -0.5 | -0.8 | 0.43 |  |
| 722513 | arrests | log_emp_index | 98 | -5.7 (3.7) | -2.6 | -5.4 | 0.75 | invalid |
| 722 | hisp_share | log_estab | 271 | -0.1 (0.2) | +0.9 | +1.1 | 0.63 |  |
| 722 | hisp_share | estab_poisson | 271 | +0.0 (0.1) | +0.7 | +1.1 | 0.02 |  |
| 722 | hisp_share | log_emp_index | 271 | +0.5 (0.7) | +2.9 | +2.0 | 0.08 | invalid |
| 722 | mexborn_share | log_estab | 271 | +0.1 (0.4) | +2.5 | +2.9 | 0.76 |  |
| 722 | mexborn_share | estab_poisson | 271 | +0.2 (0.3) | +2.1 | +2.8 | 0.22 |  |
| 722 | mexborn_share | log_emp_index | 271 | +2.4 (2.3) | +7.8 | +4.8 | 0.23 | invalid |
| 722 | arrests | log_estab | 102 | +0.6 (0.4) | +0.2 | +0.1 | 0.68 |  |
| 722 | arrests | estab_poisson | 102 | +0.1 (0.3) | -0.1 | -0.1 | 0.60 |  |
| 722 | arrests | log_emp_index | 102 | +4.8 (3.5) | +3.2 | +1.3 | 0.38 | invalid |
| 445110 | hisp_share | log_estab | 214 | -0.3 (0.3) | -0.6 | -1.1 | 0.03 |  |
| 445110 | hisp_share | estab_poisson | 214 | -0.2 (0.3) | -0.8 | -1.2 | 0.02 |  |
| 445110 | hisp_share | log_emp_index | 214 | -10.5 (4.7) | -7.9 | -12.2 | 0.66 | invalid |
| 445110 | mexborn_share | log_estab | 214 | -0.8 (0.9) | -2.1 | -3.5 | 0.04 |  |
| 445110 | mexborn_share | estab_poisson | 214 | -0.6 (0.9) | -2.6 | -3.7 | 0.05 |  |
| 445110 | mexborn_share | log_emp_index | 214 | -26.3 (12.0) | -19.0 | -28.5 | 0.42 | invalid |
| 445110 | arrests | log_estab | 81 | -0.9 (0.9) | -0.2 | -1.0 | 0.27 |  |
| 445110 | arrests | estab_poisson | 81 | -0.1 (0.7) | -0.3 | -1.2 | 0.10 |  |
| 445110 | arrests | log_emp_index | 81 | -30.1 (13.0) | -14.9 | -19.2 | 0.01 | invalid |


### A4b. Los Angeles County ZIPs, trend-adjusted (added after the pre-trend tests failed)

Exposure x linear trend estimated on 2012-2018; dev = deviation from that trend.

| NAICS | exposure | outcome | ZIPs | pre-trend per year (SE) | dev2019 (SE) | dev2022-23 (SE 2022, 2023) |
|---|---|---|---|---|---|---|
| 722511 | hisp_share | log_estab | 258 | +0.3 (0.1) | +0.2 (0.4) | +0.6 (0.9, 1.0) |
| 722511 | hisp_share | estab_poisson | 258 | +0.3 (0.1) | -0.0 (0.3) | -0.4 (0.6, 0.7) |
| 722511 | mexborn_share | log_estab | 258 | +0.5 (0.3) | +0.9 (1.1) | +2.6 (2.7, 3.1) |
| 722511 | mexborn_share | estab_poisson | 258 | +0.8 (0.2) | -0.3 (0.8) | -1.0 (1.6, 2.0) |
| 722511 | arrests | log_estab | 98 | +0.5 (0.4) | -0.2 (1.3) | -1.4 (2.4, 3.0) |
| 722511 | arrests | estab_poisson | 98 | +0.5 (0.3) | -0.2 (0.8) | -2.5 (1.2, 1.8) |
| 722513 | hisp_share | log_estab | 262 | -0.2 (0.1) | +0.1 (0.3) | +1.1 (0.8, 0.8) |
| 722513 | hisp_share | estab_poisson | 262 | -0.1 (0.1) | +0.2 (0.2) | +1.1 (0.6, 0.6) |
| 722513 | mexborn_share | log_estab | 262 | -0.5 (0.3) | +0.2 (0.8) | +2.9 (1.9, 2.1) |
| 722513 | mexborn_share | estab_poisson | 262 | -0.4 (0.2) | +0.4 (0.6) | +2.6 (1.4, 1.6) |
| 722513 | arrests | log_estab | 98 | -0.1 (0.2) | +0.1 (0.6) | +0.4 (1.3, 1.6) |
| 722513 | arrests | estab_poisson | 98 | -0.2 (0.2) | +0.1 (0.6) | -0.2 (1.4, 1.7) |
| 722 | hisp_share | log_estab | 271 | +0.0 (0.1) | -0.0 (0.3) | +1.1 (0.6, 0.6) |
| 722 | hisp_share | estab_poisson | 271 | +0.0 (0.1) | +0.2 (0.2) | +1.1 (0.4, 0.4) |
| 722 | mexborn_share | log_estab | 271 | -0.1 (0.2) | +0.0 (0.7) | +3.1 (1.6, 1.7) |
| 722 | mexborn_share | estab_poisson | 271 | +0.1 (0.1) | +0.4 (0.4) | +2.7 (1.0, 1.2) |
| 722 | arrests | log_estab | 102 | -0.2 (0.3) | +0.7 (0.6) | +1.0 (1.4, 1.6) |
| 722 | arrests | estab_poisson | 102 | +0.1 (0.1) | +0.3 (0.5) | -0.2 (0.8, 1.0) |
| 445110 | hisp_share | log_estab | 214 | -0.2 (0.1) | -0.1 (0.4) | -0.4 (1.1, 1.3) |
| 445110 | hisp_share | estab_poisson | 214 | -0.1 (0.1) | +0.0 (0.5) | -0.5 (0.9, 1.1) |
| 445110 | mexborn_share | log_estab | 214 | -0.5 (0.4) | -0.5 (1.2) | -1.4 (2.7, 3.3) |
| 445110 | mexborn_share | estab_poisson | 214 | -0.3 (0.4) | -0.4 (1.2) | -2.3 (2.4, 2.9) |
| 445110 | arrests | log_estab | 81 | -0.5 (0.4) | -0.5 (1.3) | +1.1 (2.6, 3.5) |
| 445110 | arrests | estab_poisson | 81 | -0.6 (0.3) | +0.4 (1.1) | +1.5 (2.5, 3.4) |


### A4c. City of LA ZIPs by 2010-2016 vending arrests, with and without downtown (added after seeing results)

Per log point of arrests. Downtown = ZCTAs 90012, 90013, 90014, 90015, 90017, 90021 (90071 is already out, under 1,000 residents). Implied = coefficient x sum over ZIPs of exposure x 2018 establishments: establishments against an arrest-free ZIP.

| NAICS | sample | outcome | ZIPs | estab 2018 | b2019 (SE) | b2022-23 | pre p | trend-adjusted dev2022-23 | implied estab 2019 (95%) | implied estab 2022-23 |
|---|---|---|---|---|---|---|---|---|---|---|
| 722511 | all City ZIPs | log_estab | 98 | 3344 | -0.7 (0.7) | +0.0 | 0.20 | -1.4 | -57 (-171 to +57) | +4 |
| 722511 | all City ZIPs | estab_poisson | 98 | 3344 | -0.3 (0.6) | -1.0 | 0.07 | -2.5 | -21 (-121 to +79) | -86 |
| 722511 | without downtown | log_estab | 92 | 3024 | -1.1 (0.6) | +0.5 | 0.24 | -1.3 | -72 (-147 to +4) | +34 |
| 722511 | without downtown | estab_poisson | 92 | 3024 | -0.5 (0.4) | -1.1 | 0.14 | -3.0 | -33 (-91 to +26) | -74 |
| 722513 | all City ZIPs | log_estab | 98 | 3299 | +0.2 (0.5) | -0.0 | 0.17 | +0.4 | +15 (-66 to +95) | -2 |
| 722513 | all City ZIPs | estab_poisson | 98 | 3299 | +0.0 (0.4) | -0.8 | 0.43 | -0.2 | +2 (-63 to +68) | -67 |
| 722513 | without downtown | log_estab | 92 | 3031 | +0.2 (0.6) | +1.1 | 0.01 | +1.6 | +18 (-66 to +101) | +80 |
| 722513 | without downtown | estab_poisson | 92 | 3031 | -0.0 (0.5) | +0.2 | 0.01 | +1.2 | -0 (-66 to +65) | +18 |
| 722 | all City ZIPs | log_estab | 102 | 8965 | +0.6 (0.4) | +0.1 | 0.68 | +1.0 | +135 (-58 to +328) | +32 |
| 722 | all City ZIPs | estab_poisson | 102 | 8965 | +0.1 (0.3) | -0.1 | 0.60 | -0.2 | +33 (-106 to +173) | -20 |
| 722 | without downtown | log_estab | 96 | 8132 | +0.5 (0.5) | +0.6 | 0.87 | +1.9 | +90 (-88 to +268) | +110 |
| 722 | without downtown | estab_poisson | 96 | 8132 | -0.1 (0.3) | +0.2 | 0.87 | +0.1 | -13 (-136 to +110) | +29 |
| 445110 | all City ZIPs | log_estab | 81 | 748 | -0.9 (0.9) | -1.0 | 0.27 | +1.1 | -18 (-53 to +17) | -21 |
| 445110 | all City ZIPs | estab_poisson | 81 | 748 | -0.1 (0.7) | -1.2 | 0.10 | +1.5 | -3 (-29 to +23) | -23 |
| 445110 | without downtown | log_estab | 78 | 725 | -1.1 (0.9) | -1.7 | 0.04 | +0.3 | -20 (-53 to +13) | -33 |
| 445110 | without downtown | estab_poisson | 78 | 725 | -0.2 (0.6) | -1.5 | 0.04 | +0.9 | -3 (-27 to +20) | -29 |


### A5. ZIP design in placebo counties (same specification)

| county | NAICS | exposure | outcome | ZIPs | b2019 (SE) | b2022-23 | b2012 | pre p |
|---|---|---|---|---|---|---|---|---|
| 06037 los angeles | 722511 | hisp_share | log_estab | 258 | +0.1 (0.3) | +1.4 | -1.6 | 0.05 |
| 06037 los angeles | 722511 | hisp_share | estab_poisson | 258 | +0.1 (0.2) | +0.8 | -1.8 | 0.00 |
| 06037 los angeles | 722511 | mexborn_share | log_estab | 258 | +0.5 (0.9) | +4.1 | -3.6 | 0.13 |
| 06037 los angeles | 722511 | mexborn_share | estab_poisson | 258 | -0.0 (0.7) | +2.1 | -4.9 | 0.00 |
| 06037 los angeles | 722513 | hisp_share | log_estab | 262 | +0.0 (0.2) | +0.5 | +0.8 | 0.11 |
| 06037 los angeles | 722513 | hisp_share | estab_poisson | 262 | +0.2 (0.2) | +0.7 | +0.6 | 0.02 |
| 06037 los angeles | 722513 | mexborn_share | log_estab | 262 | +0.4 (0.6) | +1.3 | +2.6 | 0.01 |
| 06037 los angeles | 722513 | mexborn_share | estab_poisson | 262 | +0.6 (0.5) | +1.4 | +2.0 | 0.00 |
| 06037 los angeles | 722 | hisp_share | log_estab | 271 | -0.1 (0.2) | +1.1 | -0.1 | 0.63 |
| 06037 los angeles | 722 | hisp_share | estab_poisson | 271 | +0.0 (0.1) | +1.1 | -0.3 | 0.02 |
| 06037 los angeles | 722 | mexborn_share | log_estab | 271 | +0.1 (0.4) | +2.9 | +0.1 | 0.76 |
| 06037 los angeles | 722 | mexborn_share | estab_poisson | 271 | +0.2 (0.3) | +2.8 | -0.6 | 0.22 |
| 06037 los angeles | 445110 | hisp_share | log_estab | 214 | -0.3 (0.3) | -1.1 | +1.3 | 0.03 |
| 06037 los angeles | 445110 | hisp_share | estab_poisson | 214 | -0.2 (0.3) | -1.2 | +1.2 | 0.02 |
| 06037 los angeles | 445110 | mexborn_share | log_estab | 214 | -0.8 (0.9) | -3.5 | +4.1 | 0.04 |
| 06037 los angeles | 445110 | mexborn_share | estab_poisson | 214 | -0.6 (0.9) | -3.7 | +2.9 | 0.05 |
| 48201 harris | 722511 | hisp_share | log_estab | 111 | -0.4 (0.5) | -1.2 | +2.9 | 0.25 |
| 48201 harris | 722511 | hisp_share | estab_poisson | 111 | -0.3 (0.4) | -0.4 | +1.7 | 0.37 |
| 48201 harris | 722511 | mexborn_share | log_estab | 111 | -1.1 (1.3) | -3.1 | +7.0 | 0.41 |
| 48201 harris | 722511 | mexborn_share | estab_poisson | 111 | -1.2 (1.1) | -1.2 | +4.9 | 0.44 |
| 48201 harris | 722513 | hisp_share | log_estab | 126 | -0.4 (0.3) | -0.1 | +1.5 | 0.19 |
| 48201 harris | 722513 | hisp_share | estab_poisson | 126 | -0.3 (0.3) | -0.3 | +1.3 | 0.20 |
| 48201 harris | 722513 | mexborn_share | log_estab | 126 | -1.3 (0.8) | -0.4 | +3.7 | 0.13 |
| 48201 harris | 722513 | mexborn_share | estab_poisson | 126 | -1.3 (0.8) | -1.2 | +3.3 | 0.23 |
| 48201 harris | 722 | hisp_share | log_estab | 126 | -0.2 (0.3) | -0.6 | +2.5 | 0.04 |
| 48201 harris | 722 | hisp_share | estab_poisson | 126 | -0.3 (0.3) | -0.5 | +1.7 | 0.03 |
| 48201 harris | 722 | mexborn_share | log_estab | 126 | -0.8 (0.7) | -1.8 | +6.2 | 0.04 |
| 48201 harris | 722 | mexborn_share | estab_poisson | 126 | -1.1 (0.7) | -1.7 | +4.6 | 0.05 |
| 48201 harris | 445110 | hisp_share | log_estab | 87 | +0.0 (0.6) | +1.3 | +0.5 | 0.03 |
| 48201 harris | 445110 | hisp_share | estab_poisson | 87 | +0.1 (0.5) | +0.9 | +1.5 | 0.04 |
| 48201 harris | 445110 | mexborn_share | log_estab | 87 | -0.2 (1.4) | +2.6 | +4.3 | 0.01 |
| 48201 harris | 445110 | mexborn_share | estab_poisson | 87 | +0.0 (1.3) | +1.9 | +4.9 | 0.02 |
| 48113 dallas | 722511 | hisp_share | log_estab | 68 | +0.8 (1.1) | +0.8 | +2.0 | 0.69 |
| 48113 dallas | 722511 | hisp_share | estab_poisson | 68 | +0.4 (0.5) | +0.6 | +1.1 | 0.71 |
| 48113 dallas | 722511 | mexborn_share | log_estab | 68 | +1.8 (2.6) | +1.8 | +6.1 | 0.31 |
| 48113 dallas | 722511 | mexborn_share | estab_poisson | 68 | +0.9 (1.1) | +0.8 | +3.8 | 0.25 |
| 48113 dallas | 722513 | hisp_share | log_estab | 77 | +0.1 (0.5) | -0.9 | -0.5 | 0.04 |
| 48113 dallas | 722513 | hisp_share | estab_poisson | 77 | +0.0 (0.4) | -0.3 | -0.5 | 0.18 |
| 48113 dallas | 722513 | mexborn_share | log_estab | 77 | -0.3 (1.1) | -2.9 | -1.3 | 0.37 |
| 48113 dallas | 722513 | mexborn_share | estab_poisson | 77 | -0.3 (0.8) | -1.5 | -1.7 | 0.41 |
| 48113 dallas | 722 | hisp_share | log_estab | 80 | -0.3 (0.5) | -1.0 | -1.0 | 0.00 |
| 48113 dallas | 722 | hisp_share | estab_poisson | 80 | -0.1 (0.3) | +0.2 | -0.1 | 0.42 |
| 48113 dallas | 722 | mexborn_share | log_estab | 80 | -1.0 (1.1) | -3.4 | -1.7 | 0.06 |
| 48113 dallas | 722 | mexborn_share | estab_poisson | 80 | -0.4 (0.6) | -0.9 | -0.1 | 0.85 |
| 48113 dallas | 445110 | hisp_share | log_estab | 54 | +1.6 (1.0) | +0.3 | +3.2 | 0.05 |
| 48113 dallas | 445110 | hisp_share | estab_poisson | 54 | +1.8 (0.8) | +0.9 | +3.0 | 0.02 |
| 48113 dallas | 445110 | mexborn_share | log_estab | 54 | +3.7 (2.4) | +1.0 | +12.2 | 0.06 |
| 48113 dallas | 445110 | mexborn_share | estab_poisson | 54 | +4.2 (2.0) | +2.3 | +10.1 | 0.02 |
| 48029 bexar | 722511 | hisp_share | log_estab | 56 | -0.4 (0.8) | -1.8 | +0.4 | 0.03 |
| 48029 bexar | 722511 | hisp_share | estab_poisson | 56 | -0.1 (0.8) | -0.7 | -0.1 | 0.00 |
| 48029 bexar | 722511 | mexborn_share | log_estab | 56 | -0.1 (3.3) | -7.9 | +4.0 | 0.13 |
| 48029 bexar | 722511 | mexborn_share | estab_poisson | 56 | -0.3 (3.3) | -6.9 | +0.3 | 0.01 |
| 48029 bexar | 722513 | hisp_share | log_estab | 56 | -0.3 (0.8) | -0.3 | +3.4 | 0.01 |
| 48029 bexar | 722513 | hisp_share | estab_poisson | 56 | +0.7 (0.4) | -0.2 | +2.2 | 0.01 |
| 48029 bexar | 722513 | mexborn_share | log_estab | 56 | -1.8 (2.6) | +0.4 | +11.8 | 0.03 |
| 48029 bexar | 722513 | mexborn_share | estab_poisson | 56 | +0.6 (1.9) | -0.6 | +9.1 | 0.02 |
| 48029 bexar | 722 | hisp_share | log_estab | 63 | -0.2 (0.6) | -2.1 | +3.5 | 0.00 |
| 48029 bexar | 722 | hisp_share | estab_poisson | 63 | +0.2 (0.4) | -0.3 | +1.8 | 0.02 |
| 48029 bexar | 722 | mexborn_share | log_estab | 63 | -1.4 (2.3) | -11.1 | +13.9 | 0.03 |
| 48029 bexar | 722 | mexborn_share | estab_poisson | 63 | -0.3 (1.6) | -3.5 | +9.1 | 0.10 |
| 04013 maricopa | 722511 | hisp_share | log_estab | 110 | -0.5 (0.6) | -0.6 | -1.8 | 0.24 |
| 04013 maricopa | 722511 | hisp_share | estab_poisson | 110 | -0.4 (0.6) | -0.6 | -0.1 | 0.68 |
| 04013 maricopa | 722511 | mexborn_share | log_estab | 110 | -1.2 (1.6) | -3.0 | -2.0 | 0.46 |
| 04013 maricopa | 722511 | mexborn_share | estab_poisson | 110 | -1.2 (1.6) | -3.6 | +1.9 | 0.63 |
| 04013 maricopa | 722513 | hisp_share | log_estab | 110 | +0.5 (0.4) | -0.1 | +0.7 | 0.05 |
| 04013 maricopa | 722513 | hisp_share | estab_poisson | 110 | +0.7 (0.3) | +0.4 | +0.9 | 0.13 |
| 04013 maricopa | 722513 | mexborn_share | log_estab | 110 | +1.5 (1.0) | -0.7 | +3.1 | 0.01 |
| 04013 maricopa | 722513 | mexborn_share | estab_poisson | 110 | +1.9 (0.9) | -0.3 | +2.4 | 0.07 |
| 04013 maricopa | 722 | hisp_share | log_estab | 119 | +0.4 (0.3) | +0.7 | +0.2 | 0.85 |
| 04013 maricopa | 722 | hisp_share | estab_poisson | 119 | +0.1 (0.3) | +0.6 | +0.7 | 0.13 |
| 04013 maricopa | 722 | mexborn_share | log_estab | 119 | +0.9 (0.9) | +0.1 | +1.6 | 0.68 |
| 04013 maricopa | 722 | mexborn_share | estab_poisson | 119 | +0.2 (0.7) | -0.5 | +2.5 | 0.05 |
| 04013 maricopa | 445110 | hisp_share | log_estab | 66 | +0.4 (0.8) | -1.0 | +2.4 | 0.12 |
| 04013 maricopa | 445110 | hisp_share | estab_poisson | 66 | +0.3 (0.8) | -1.0 | +2.6 | 0.35 |
| 04013 maricopa | 445110 | mexborn_share | log_estab | 66 | +0.7 (2.2) | -2.5 | +7.6 | 0.11 |
| 04013 maricopa | 445110 | mexborn_share | estab_poisson | 66 | +0.1 (2.2) | -2.8 | +7.9 | 0.37 |
| 17031 cook | 722511 | hisp_share | log_estab | 140 | +0.0 (0.4) | +2.1 | -0.7 | 0.28 |
| 17031 cook | 722511 | hisp_share | estab_poisson | 140 | +0.4 (0.4) | +2.4 | -1.6 | 0.16 |
| 17031 cook | 722511 | mexborn_share | log_estab | 140 | +0.0 (1.1) | +5.2 | -2.0 | 0.60 |
| 17031 cook | 722511 | mexborn_share | estab_poisson | 140 | +0.7 (0.9) | +6.1 | -3.1 | 0.36 |
| 17031 cook | 722513 | hisp_share | log_estab | 150 | -0.1 (0.5) | +0.3 | -0.2 | 0.56 |
| 17031 cook | 722513 | hisp_share | estab_poisson | 150 | +0.2 (0.4) | +0.1 | +0.6 | 0.76 |
| 17031 cook | 722513 | mexborn_share | log_estab | 150 | -0.2 (1.4) | +1.1 | -0.5 | 0.45 |
| 17031 cook | 722513 | mexborn_share | estab_poisson | 150 | +0.8 (1.1) | +0.2 | +1.4 | 0.45 |
| 17031 cook | 722 | hisp_share | log_estab | 157 | +0.1 (0.4) | +1.7 | -0.6 | 0.29 |
| 17031 cook | 722 | hisp_share | estab_poisson | 157 | +0.3 (0.3) | +1.4 | -0.9 | 0.28 |
| 17031 cook | 722 | mexborn_share | log_estab | 157 | +0.3 (1.0) | +4.8 | -1.4 | 0.49 |
| 17031 cook | 722 | mexborn_share | estab_poisson | 157 | +0.7 (0.6) | +3.6 | -1.4 | 0.45 |
| 17031 cook | 445110 | hisp_share | log_estab | 111 | +0.2 (0.4) | +0.4 | -0.6 | 0.70 |
| 17031 cook | 445110 | hisp_share | estab_poisson | 111 | +0.5 (0.4) | +0.6 | -0.4 | 0.54 |
| 17031 cook | 445110 | mexborn_share | log_estab | 111 | +0.3 (1.0) | +0.1 | -3.3 | 0.72 |
| 17031 cook | 445110 | mexborn_share | estab_poisson | 111 | +0.9 (0.9) | +0.7 | -2.2 | 0.32 |
| 12086 miamidade | 722511 | hisp_share | log_estab | 66 | -1.2 (0.7) | -2.1 | +0.5 | 0.40 |
| 12086 miamidade | 722511 | hisp_share | estab_poisson | 66 | -1.0 (0.7) | -2.1 | +1.1 | 0.56 |
| 12086 miamidade | 722511 | mexborn_share | log_estab | 66 | -4.9 (12.1) | +6.2 | -6.3 | 0.02 |
| 12086 miamidade | 722511 | mexborn_share | estab_poisson | 66 | -0.5 (9.9) | +1.9 | -5.1 | 0.15 |
| 12086 miamidade | 722513 | hisp_share | log_estab | 68 | +0.2 (0.5) | -1.7 | -0.8 | 0.69 |
| 12086 miamidade | 722513 | hisp_share | estab_poisson | 68 | +0.1 (0.5) | -2.2 | -1.0 | 0.59 |
| 12086 miamidade | 722513 | mexborn_share | log_estab | 68 | -6.2 (6.1) | -9.1 | -19.2 | 0.00 |
| 12086 miamidade | 722513 | mexborn_share | estab_poisson | 68 | -1.8 (5.2) | -3.9 | -14.5 | 0.00 |
| 12086 miamidade | 722 | hisp_share | log_estab | 71 | -0.2 (0.4) | -1.7 | -0.8 | 0.68 |
| 12086 miamidade | 722 | hisp_share | estab_poisson | 71 | -0.5 (0.4) | -2.2 | -0.5 | 0.91 |
| 12086 miamidade | 722 | mexborn_share | log_estab | 71 | +4.1 (3.4) | +5.4 | -2.3 | 0.95 |
| 12086 miamidade | 722 | mexborn_share | estab_poisson | 71 | +2.8 (3.8) | +4.5 | -2.3 | 0.01 |
| 12086 miamidade | 445110 | hisp_share | log_estab | 62 | -0.4 (0.7) | +0.6 | -1.4 | 0.14 |
| 12086 miamidade | 445110 | hisp_share | estab_poisson | 62 | +0.2 (0.6) | +0.7 | -0.6 | 0.12 |
| 12086 miamidade | 445110 | mexborn_share | log_estab | 62 | -1.1 (4.1) | -0.4 | -44.2 | 0.00 |
| 12086 miamidade | 445110 | mexborn_share | estab_poisson | 62 | +1.7 (3.2) | -1.0 | -18.1 | 0.00 |


### A6. Taxable sales (CDTFA), every specification

Per 10 points of the share. l_c08 food services and drinking places; l_c04 food and beverage stores (placebo); l_diff their difference; l_permits C08 seller's permits (cities: outlets) in Q4.

| level | exposure | outcome | weight | units | b2019 (SE) | b2020-21 | b2022-23 | b2024-25 | pre p |
|---|---|---|---|---|---|---|---|---|---|
| county | hisp_share | l_c08 | none | 56 | +0.1 (0.1) | +2.7 | +2.6 | +3.0 | 0.04 |
| county | hisp_share | l_c08 | pop | 56 | +0.1 (0.1) | +4.1 | +2.5 | +2.2 | 0.08 |
| county | hisp_share | l_c04 | none | 56 | +0.1 (0.3) | -0.0 | +0.6 | +0.9 | 0.00 |
| county | hisp_share | l_c04 | pop | 56 | +0.5 (0.2) | +1.8 | +3.1 | +3.1 | 0.25 |
| county | hisp_share | l_diff | none | 56 | -0.0 (0.3) | +2.7 | +2.0 | +2.1 | 0.00 |
| county | hisp_share | l_diff | pop | 56 | -0.3 (0.3) | +2.4 | -0.6 | -0.9 | 0.03 |
| county | hisp_share | l_permits | none | 56 | +0.2 (0.3) | +0.7 | +1.9 | +2.8 | 0.12 |
| county | hisp_share | l_permits | pop | 56 | +0.6 (0.3) | +1.5 | +2.5 | +3.8 | 0.27 |
| county | mexborn_share | l_c08 | none | 56 | +0.7 (0.5) | +6.2 | +6.3 | +7.4 | 0.06 |
| county | mexborn_share | l_c08 | pop | 56 | +0.2 (0.4) | +11.6 | +7.6 | +6.8 | 0.52 |
| county | mexborn_share | l_c04 | none | 56 | +0.5 (1.0) | +0.3 | +1.6 | +2.7 | 0.00 |
| county | mexborn_share | l_c04 | pop | 56 | +1.4 (0.8) | +5.1 | +9.1 | +9.3 | 0.25 |
| county | mexborn_share | l_diff | none | 56 | +0.3 (1.1) | +6.0 | +4.7 | +4.7 | 0.00 |
| county | mexborn_share | l_diff | pop | 56 | -1.2 (0.9) | +6.4 | -1.5 | -2.5 | 0.10 |
| county | mexborn_share | l_permits | none | 56 | +0.1 (0.8) | +1.2 | +3.8 | +5.7 | 0.06 |
| county | mexborn_share | l_permits | pop | 56 | +1.0 (0.9) | +3.4 | +6.2 | +9.0 | 0.20 |
| city | hisp_share | l_c08 | none | 80 | +0.2 (0.2) | +2.8 | +0.5 | +0.8 | 0.36 |
| city | hisp_share | l_c08 | pop | 80 | +0.3 (0.2) | +3.4 | +1.2 | +1.3 | 0.15 |
| city | hisp_share | l_c04 | none | 80 | -0.5 (0.2) | -0.2 | +0.3 | +0.9 | 0.29 |
| city | hisp_share | l_c04 | pop | 80 | -0.2 (0.1) | +0.1 | +0.5 | +0.8 | 0.10 |
| city | hisp_share | l_diff | none | 80 | +0.7 (0.3) | +3.0 | +0.3 | -0.1 | 0.10 |
| city | hisp_share | l_diff | pop | 80 | +0.5 (0.2) | +3.3 | +0.7 | +0.6 | 0.00 |
| city | hisp_share | l_permits | none | 80 | +0.2 (0.2) | +0.8 | +1.4 | +1.5 | 0.10 |
| city | hisp_share | l_permits | pop | 80 | +0.1 (0.2) | +0.7 | +1.1 | +1.1 | 0.00 |
| city | mexborn_share | l_c08 | none | 80 | +0.6 (0.4) | +7.4 | +1.5 | +2.0 | 0.17 |
| city | mexborn_share | l_c08 | pop | 80 | +0.7 (0.4) | +7.5 | +2.4 | +2.9 | 0.08 |
| city | mexborn_share | l_c04 | none | 80 | -0.6 (0.4) | -0.5 | +0.1 | +1.8 | 0.71 |
| city | mexborn_share | l_c04 | pop | 80 | -0.3 (0.4) | -0.4 | +0.4 | +1.1 | 0.17 |
| city | mexborn_share | l_diff | none | 80 | +1.2 (0.6) | +7.9 | +1.4 | +0.2 | 0.17 |
| city | mexborn_share | l_diff | pop | 80 | +1.1 (0.6) | +7.9 | +2.0 | +1.8 | 0.00 |
| city | mexborn_share | l_permits | none | 80 | +0.6 (0.4) | +2.1 | +3.9 | +4.0 | 0.09 |
| city | mexborn_share | l_permits | pop | 80 | +0.6 (0.5) | +2.0 | +3.0 | +2.6 | 0.01 |

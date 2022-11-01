# newDisguiser

The newDisguiser is an extensive measurement build atop of [Disguiser](https://github.com/e2ecensor/Disguiser_public), an end-to-end, ground truth based framework for measuring Internet censorship.

The newDisguiser deploys multiple geo-distributed backend control servers. As such, within a country, the packets that carry the same test domain but with different destination IPs may be forced to traverse different border networks to identify the censorship activity on each path for one vantage point, thereby quantifying the censorship diversity caused by the different paths and ISP networks in one country.

The collected data by this enhanced setting can be downloaded at [here](https://drive.google.com/drive/folders/1vZ7JuQsWQYIKkT8hxX-_qRldjnSuykQy).

### Data

The explortary data includes identified results of censorship activities for the paths from one vantage points to each of multiple backend control servers.

### Analysis Code

The analysis scripts aim to identify the inconsistency experiened by different paths toward different backend control servers from one vantage point.

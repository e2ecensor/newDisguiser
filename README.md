# newDisguiser

The newDisguiser is an extensive measurement build atop of [Disguiser](https://github.com/e2ecensor/Disguiser_public), an end-to-end, ground truth based framework for measuring Internet censorship.

The newDisguiser deploys multiple geo-distributed backend control servers. As such, within a country, the packets that carry the same test domain but with different destination IPs may be forced to traverse different border networks to identify the censorship activity on each path for one vantage point, thereby quantifying the censorship diversity caused by the different paths and ISP networks in one country.

### Data

The explortary data includes identified results of censorship activities for the paths from one vantage points to each of multiple backend control servers. The collected raw data by this enhanced setting can be downloaded at [here](https://drive.google.com/drive/folders/1vZ7JuQsWQYIKkT8hxX-_qRldjnSuykQy).


### Analysis Code

The analysis scripts aim to identify the inconsistency experiened by different paths toward different backend control servers from one vantage point.

Code repository:
- http_censorship.py: this code is for analyzing the total detected censorship and categorize by countries.
- http_server_censorship.py: this code is utilized in the experiment for censorship measurements from distributed vantage points to control servers from different cloud services.
- http_suspicious_server.py: this code is for analyzing censorship diversity in different paths from various vantage points towards control servers that belongs to different cloud services.

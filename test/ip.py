import requests

def get(ip):
	r = requests.get(f"http://ip-api.com/json/{ip}")
	print(r)
	print(f'{ip}\t{r.json().get("country", "empty")}\t{r.json().get("regionName", "empty")}\t{r.json().get("city", "empty")}\n'+ \
				f'\t{r.json().get("zip", "empty")}\t{r.json().get("lat", "empty")}\t{r.json().get("lon", "empty")}\n' +\
				f'\t{r.json().get("isp", "empty")}\t{r.json().get("as", "empty")}\n' +\
				f'\t{r.json().get("asname", "empty")}\t{r.json().get("mobile", "empty")}\n')

get("192.168.96.1")
get("129.13.55.209")
get("193.196.36.1")
get("141.52.3.6")
get("193.197.63.6")
get("129.143.60.115")
get("129.143.200.42")
get("62.53.11.130")
get("62.53.0.198")
get("62.53.4.213")
get("62.53.8.31")
get("62.53.2.159")
get("46.114.149.213")
get("185.52.247.41")
get("87.137.247.61")
get("93.199.153.203")
get("80.157.200.197")
get("46.114.148.852")
get("46.114.151.161")
get("46.114.151.192")
get("62.53.11.132")
get("62.53.28.154")
get("62.53.3.53")
get("62.53.8.37")
get("62.53.2.127")
get("192.168.80.1")
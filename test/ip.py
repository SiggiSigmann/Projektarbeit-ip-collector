import requests


def get(ip):
	r = requests.get(f"http://ip-api.com/json/{ip}")
	print(r)
	print(f'{ip}\t{r.json().get("country", "empty")}\t{r.json().get("regionName", "empty")}\t{r.json().get("city", "empty")}\n'+ \
				f'\t{r.json().get("zip", "empty")}\t{r.json().get("lat", "empty")}\t{r.json().get("lon", "empty")}\n' +\
				f'\t{r.json().get("isp", "empty")}\t{r.json().get("as", "empty")}\n' +\
				f'\t{r.json().get("asname", "empty")}\t{r.json().get("mobile", "empty")}\n')

count = 0

f = open('file.txt','r')
while True:
	x = f.readline()
	ar = x.split()
	if not ar: break
	if count > 3:
		get(ar[1])
		for i in range(9999999):
			continue
	count += 1



f.close()


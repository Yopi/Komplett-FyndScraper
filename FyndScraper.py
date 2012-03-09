from lxml import etree 
import urllib2, time, socket, random

fyndsidor = ("http://www.komplett.se/k/kl.aspx?bn=10072", "http://www.komplett.se/k/kl.aspx?bn=10073", "http://www.komplett.se/k/kl.aspx?bn=11203", "http://www.komplett.se/k/kl.aspx?bn=10071", "http://www.komplett.se/k/kl.aspx?bn=10076")
#fyndsidor = ("test.html", "test2.html")
def parse_sida(url, comp=None):
  request_page = urllib2.Request(url)
  result = urllib2.urlopen(request_page)
  html = etree.HTML(result.read())
#  result = open(url, "r")
#  html = etree.HTML(result.read())

  namn = html.xpath('//table//td[@class="prod-name"]//h4/a/text()')
  pris = html.xpath('//table//td[@class="prices"]//strong/text()');
  adress = html.xpath('//table//td[@class="prod-name"]//h4/a/@href')

  if comp is not None:
    nya_saker = list(set(namn) - set(comp[0]))
    for item in nya_saker:
      index = namn.index(item)
      print "Ny skit: %s kostar %s | %s" % (namn[index], pris[index], adress[index])
      skicka_irc(namn[index], pris[index], adress[index])
  return [namn, pris, adress]

def skicka_irc(namn, pris, adress):
  s = socket.socket()
  s.connect(("localhost", 1551))
  s.send("Ny vara: "+namn+" kostar "+pris+" | "+adress)
  s.close()

items=[None]*len(fyndsidor)
while True:
  for i in range(len(fyndsidor)):
    items[i] = parse_sida(fyndsidor[i], items[i])
  time.sleep(60*4 + random.random()*60)
#  time.sleep(5)

from urllib.parse import urlparse

link1 = "https://www.theguardian.com/politics/2023/feb/11/revealed-secret-cross-party-summit-held-to-confront-failings-of-brexit"
link2 = "https://www.theguardian.com/politics/2023/feb/11/revealed-secret-cross-party-summit-held-to-confront-failings-of-brexit?CMP=share_btn_tw"

parsed_link1 = urlparse(link1)
parsed_link2 = urlparse(link2)

if parsed_link1.scheme == parsed_link2.scheme and parsed_link1.netloc == parsed_link2.netloc and parsed_link1.path == parsed_link2.path:
    print("The links have similar URL structures.")
else:
    print("The links have different URL structures.")

import hmac
from dataclasses import dataclass, field, asdict
import random
from pprint import pprint

import requests


@dataclass
class PurchaseData:
    merchantAccount: str
    merchantDomainName: str
    orderReference: str
    orderDate: str
    amount: str
    currency: str


@dataclass
class ProductData:
    productName: str
    productCount: str
    productPrice: str


class WFPClient:
    """
    https://wiki.wayforpay.com/view/852102 - тут опис усіх аргументів для запиту
    """
    url = 'https://secure.wayforpay.com/pay?behavior=offline'
    SecretKey = 'flk3409refn54t54t*FNJRET'

    def __init__(self, data: PurchaseData, products: list[ProductData], **kwargs):
        self.data = data
        self.products = products
        self.response = None
        self.request_data = self.get_request_data()
        self.request_data['merchantSignature'] = self._get_has_md5()
        self.request_data.update(kwargs)

    def to_request(self, url=None):
        self.response = requests.post(
            url or self.url,
            data=self.request_data)

    def get_request_data(self) -> dict:
        request_dict = asdict(self.data)
        for num, pr in enumerate(self.products):
            request_dict[f'productName[{num}]'] = pr.productName
            request_dict[f'productPrice[{num}]'] = pr.productPrice
            request_dict[f'productCount[{num}]'] = pr.productCount
        return request_dict

    def _get_hash_products_str(self):
        products = [asdict(pr).values() for pr in self.products]
        return ';'.join([';'.join(pr) for pr in zip(*products)])

    def _get_hash_str(self):
        return ';'.join(asdict(self.data).values()) + ';' + self._get_hash_products_str()

    def _get_has_md5(self):
        return hmac.new(
            self.SecretKey.encode('utf-8'),
            self._get_hash_str().encode('utf-8'),
            'MD5'
        ).hexdigest()


if __name__ == '__main__':
    pd = PurchaseData(
        merchantAccount='test_merch_n1',
        merchantDomainName="www.market.ua",
        orderReference=f"DH{random.randint(1000, 99999)}",
        orderDate="1415379863",
        amount="1",
        currency="UAH",
    )
    pr = [
        ProductData(
            productName="Процессор Intel Core i5-4670 3.4GHz",
            productPrice="10",
            productCount="1",
        ),
        ProductData(
            productName="Память Kingston DDR3-1600 4096MB PC3-12800",
            productPrice="55",
            productCount="12",
        ),
    ]

    client = WFPClient(data=pd, products=pr, language='ua')
    client.to_request()
    pprint(client.request_data)
    print(client.response.text)

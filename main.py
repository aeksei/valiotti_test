"""
Скрипт для скачивания сделок через API amoCRM

Скрипт обращается к API amoCRM и забирает последние 30 сделок,
сохраняет их в pandas dataframe.

Скрипт можно запустить в двух режимах: рабочем и тестирования
Запуск скрипта в режиме проверки парсинга json ответа от API: python main.py --test

В функции main подготовлен доступ для скачивания json файла от API amoCRM

"""
import os.path
import json
import argparse
import requests

import pandas as pd

SUBDOMAIN = "TEST"
IS_TEST = True
JSON_FILE = 'test_file.json'


def main():
    """
    Функция работает в двух режимах. Чтобы запустить режим тестирования нужно либо установить константу IS_TEST
    либо запустить скрипт следующим образом: python main.py --test

    В остальном программа пытается подключиться к API amoCRM к поддомену SUBDOMAIN
    :return:
    """
    parser = create_parser()
    args = parser.parse_args()

    subdomain = SUBDOMAIN if args.subdomain is None else args.subdomain
    is_test = IS_TEST if args.test is None else args.test

    if not is_test:
        url = get_leads_url(subdomain)
        headers = {'content-type': 'application/json',
                   'user-agent': 'amoCRM-API-client/1.0'}

        resp = requests.get(url, headers=headers)
        parse_leads(resp.json())
    else:
        if not os.path.exists(JSON_FILE):
            create_test_json_file(JSON_FILE)
        with open(JSON_FILE) as f:
            json_obj = json.load(f)
        df = parse_leads(json_obj)
        print(df)


def get_leads_url(subdomain, limit_rows: int = 30) -> str:
    """
    Функция для формировавания url для доступа к сделкам

    Первый аргумент должен быть формата "?first_arg="
    Добавление второго и последующих аргументов должно быть формата "&second_arg="

    :param subdomain: subdomain for access
    :param limit_rows: count selected rows
    :return:
    """

    base_url = f'https://{subdomain}.amocrm.ru/api/v2/leads'
    base_url += f'?limit_rows={limit_rows}'

    return base_url


def parse_leads(json_obj):
    """
    Функция, обрабатывающая json и возвращающая pandas DataFrame содержащий сделки

    В строках указываются сделки, колонки ключи из json
    Ключи, содержащие простые значения добавлются в явном виде
    Ключи с составными значениями берется значение с самым глубоким уровнем вложенности

    :param json_obj: json prepare to parse
    :return: pandas DataFrame
    """
    simple_keys = ['id', 'name', 'responsible_user_id', 'created_by', 'created_at',
                   'updated_at', 'account_id', 'is_deleted', 'group_id', 'closed_at',
                   'closest_task_at', 'status_id', 'sale']
    composite_keys = ['main_contact', 'company', 'tags', 'custom_fields',
                      'contacts', 'pipeline', '_links']

    df = pd.DataFrame()

    for item in json_obj['_embedded']['items']:
        # parse composite_keys
        # TODO tags
        # TODO custom_fields
        dict_ = {}
        dict_.update({'main_contact__id': item['main_contact']['id'],
                      'main_contact__href': item['main_contact']['_links']['self']['href']
                      })

        dict_.update({'company__id': item['company']['id'],
                      'company__name': item['company']['name'],
                      'company__href': item['company']['_links']['self']['href']
                      })

        dict_.update({'contacts__id': ",".join(map(str, item['contacts']['id'])),
                      'contacts__href': item['contacts']['_links']['self']['href']
                      })

        dict_.update({'pipeline__id': item['pipeline']['id'],
                      'pipeline__href': item['pipeline']['_links']['self']['href']
                      })

        dict_.update({'href': item['_links']['self']['href']})

        # add dict with simple keys list
        dict_.update({key: item[key] for key in simple_keys})

        df = df.append(pd.DataFrame([dict_]))  # add new row with transaction info

    return df


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--subdomain',
                        type=str,
                        default=None,
                        help='Поддомен для доступа')
    parser.add_argument('--test',
                        action='store_const',
                        const=True,
                        default=None,
                        help='Включить режим тестирования парсинга json')

    return parser


def create_test_json_file(filename):
    """
    Создание тестового файла с json объектом для проверки
    :param filename:
    :return:
    """
    json_obj = {
        "_links": {
            "self": {
                "href": "/api/v2/leads?id=1090256",
                "method": "get"
            }
        },
        "_embedded": {
            "items": [
                {
                    "id": 1090256,
                    "name": "Сделка #1090256",
                    "responsible_user_id": 957084,
                    "created_by": 957084,
                    "created_at": 1508400624,
                    "updated_at": 1508403644,
                    "account_id": 13670640,
                    "is_deleted": False,
                    "main_contact": {
                        "id": 1099418,
                        "_links": {
                            "self": {
                                "href": "/api/v2/contacts?id=1099153",
                                "method": "get"
                            }
                        }
                    },
                    "group_id": 0,
                    "company": {
                        "id": 1099427,
                        "name": None,
                        "_links": {
                            "self": {
                                "href": "/api/v2/companies?id=1099152",
                                "method": "get"
                            }
                        }
                    },
                    "closed_at": 0,
                    "closest_task_at": 1508446740,
                    "tags": [

                    ],
                    "custom_fields": [
                        {
                            "id": 4399664,
                            "name": "Список",
                            "values": [
                                {
                                    "value": "5",
                                    "enum": "3691641"
                                }
                            ],
                            "is_system": False
                        },
                        {
                            "id": 4399665,
                            "name": "Мультисписок",
                            "values": [
                                {
                                    "value": "2",
                                    "enum": "3691643"
                                },
                                {
                                    "value": "3",
                                    "enum": "3691644"
                                }
                            ],
                            "is_system": False
                        },
                        {
                            "id": 4399666,
                            "name": "Текст",
                            "values": [
                                {
                                    "value": "Здесь, к примеру, какие-либо пояснения к сделке"
                                }
                            ],
                            "is_system": False
                        },
                        {
                            "id": 4399663,
                            "name": "Адрес",
                            "values": [
                                {
                                    "value": "пр-т Мира, д. 3",
                                    "subtype": "1"
                                },
                                {
                                    "value": "Москва",
                                    "subtype": "3"
                                },
                                {
                                    "value": "101010",
                                    "subtype": "5"
                                }
                            ],
                            "is_system": False
                        }
                    ],
                    "contacts": {
                        "id": [
                            1099418,
                            1099154
                        ],
                        "_links": {
                            "self": {
                                "href": "/api/v2/contacts?id=1099418,1099154",
                                "method": "get"
                            }
                        }
                    },
                    "status_id": 13670642,
                    "sale": 5000,
                    "pipeline": {
                        "id": 10273,
                        "_links": {
                            "self": {
                                "href": "/api/v2/pipelines?id=10246",
                                "method": "get"
                            }
                        }
                    },
                    "_links": {
                        "self": {
                            "href": "/api/v2/leads?id=1090256",
                            "method": "get"
                        }
                    }
                }
            ]
        }
    }

    with open(filename, 'w') as f:
        json.dump(json_obj, f, indent=4)


if __name__ == "__main__":
    main()

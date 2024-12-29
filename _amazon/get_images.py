# -*- coding: utf-8 -*-

"""
 Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License").
 You may not use this file except in compliance with the License.
 A copy of the License is located at

     http://www.apache.org/licenses/LICENSE-2.0

 or in the "license" file accompanying this file. This file is distributed
 on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 express or implied. See the License for the specific language governing
 permissions and limitations under the License.
"""

"""
 ProductAdvertisingAPI

 https://webservices.amazon.com/paapi5/documentation/index.html

"""

"""
This sample code snippet is for ProductAdvertisingAPI 5.0's GetItems API

For more details, refer:
https://webservices.amazon.com/paapi5/documentation/get-items.html

"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.condition import Condition
from paapi5_python_sdk.models.get_items_request import GetItemsRequest
from paapi5_python_sdk.models.get_items_resource import GetItemsResource
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.rest import ApiException


def parse_response(item_response_list):
    """
    The function parses GetItemsResponse and creates a dict of ASIN to Item object
    :param item_response_list: List of Items in GetItemsResponse
    :return: Dict of ASIN to Item object
    """
    mapped_response = {}
    for item in item_response_list:
        mapped_response[item.asin] = item
    return mapped_response


def get_items(access_key, secret_key, partner_tag, all_item_ids):
    """ PAAPI host and region to which you want to send request """
    """ For more details refer: https://webservices.amazon.com/paapi5/documentation/common-request-parameters.html#host-and-region"""
    host = "webservices.amazon.com"
    region = "us-east-1"

    """ API declaration """
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    """ Request initialization"""

    """ Choose item id(s) """


    """ Choose resources you want from GetItemsResource enum """
    """ For more details, refer: https://webservices.amazon.com/paapi5/documentation/get-items.html#resources-parameter """
    get_items_resource = [
        GetItemsResource.IMAGES_PRIMARY_MEDIUM
    ]

    """ Forming request """
    output_arr = []

    for i in range(0, len(all_item_ids), 10):
        item_ids = all_item_ids[i:i+10]
        try:
            get_items_request = GetItemsRequest(
                partner_tag=partner_tag,
                partner_type=PartnerType.ASSOCIATES,
                marketplace="www.amazon.com",
                condition=Condition.NEW,
                item_ids=item_ids,
                resources=get_items_resource,
            )
        except ValueError as exception:
            print("Error in forming GetItemsRequest: ", exception)
            return
        try:
            """ Sending request """
            response = default_api.get_items(get_items_request)

            print("API called Successfully")
            #print("Complete Response:", response)

            """ Parse response """
            if response.items_result is not None:
                print("Printing all item information in ItemsResult:")
                response_list = parse_response(response.items_result.items)
                for item_id in item_ids:
                    print("Printing information about the item_id: ", item_id)
                    if item_id in response_list:
                        item = response_list[item_id]
                        if item is not None:
                            if item.images is not None:
                                print("Image url: ", item.images.primary.medium.url)
                                output_arr.append({"id": item_id, "img": item.images.primary.medium.url})
                    else:
                        print("Item not found, check errors")

            if response.errors is not None:
                print("\nPrinting Errors:\nPrinting First Error Object from list of Errors")
                print("Error code", response.errors[0].code)
                print("Error message", response.errors[0].message)

        except ApiException as exception:
            print("Error calling PA-API 5.0!")
            print("Status code:", exception.status)
            print("Errors :", exception.body)
            print("Request ID:", exception.headers["x-amzn-RequestId"])
            return

        except TypeError as exception:
            print("TypeError :", exception)

        except ValueError as exception:
            print("ValueError :", exception)

        except Exception as exception:
            print("Exception :", exception)

    with open('_data/ids_to_imgs.json', 'w') as f:
        json.dump(output_arr, f)


if __name__ == "__main__":
    import sys

    access_key = sys.argv[1]
    secret_key = sys.argv[2]
    partner_tag = sys.argv[3]

    import json

    # Open the JSON file
    with open('_data/item_ids.json', 'r') as f:
        # Load the JSON data into a Python dictionary
        data = json.load(f)
        item_ids = data["ids"]
        get_items(access_key, secret_key, partner_tag, item_ids)
# get_items_with_http_info()
# get_items_async()

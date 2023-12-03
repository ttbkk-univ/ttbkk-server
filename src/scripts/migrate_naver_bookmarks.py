import json
import os
from typing import cast

from src.apps.place.models import Place
from src.crawlers.franchise_type import FranchiseType


def run(file_name: str = "naver_bookmark.json", ttbkk_category_name: str = "떡볶이"):
    json_file = os.path.join(os.path.dirname(__file__), file_name)

    data = json.load(open(json_file, "r", encoding="utf-8"))

    filtered_forders = [forder for forder in cast(list[dict], data.get('my').get('folderSync').get("folders")) if
                        forder.get('name') == ttbkk_category_name]

    if len(filtered_forders) == 0:
        raise Exception(f"{ttbkk_category_name} 그룹이 존재하지 않습니다.")

    if len(filtered_forders) > 1:
        raise Exception(f"{ttbkk_category_name} 그룹이 2개 이상 존재합니다.")

    ttbkk_folder = filtered_forders[0]

    # filter by category_name
    category_filtered_bookmarks = list(map(
        lambda bookmark: bookmark.get("bookmark"),
        filter(
            lambda bookmark: len(list(filter(
                lambda folder_mapping: folder_mapping.get("folderId") == ttbkk_folder.get("folderId"),
                bookmark.get("folderMappings"),
            ))) > 0,
            cast(list[dict], data.get('my').get('bookmarkSync').get("bookmarks")),
        ),
    ))

    # filter by FranchiseType
    franchise_type_filtered_bookmarks = list(filter(
        lambda bookmark: not len(list(filter(lambda type: type.value in bookmark.get("name"), FranchiseType))),
        category_filtered_bookmarks,
    ))

    places = []
    for bookmark in franchise_type_filtered_bookmarks:
        bookmarkId = bookmark.get("bookmarkId")  # : 1325377011,
        name = bookmark.get("name")  # : "레드175 대치역점",
        displayName = bookmark.get("displayName")  # : "",
        px = bookmark.get("px")  # : 127.0624408,
        py = bookmark.get("py")  # : 37.4938266,
        type = bookmark.get("type")  # : "place",
        useTime = bookmark.get("useTime")  # : 1701597577000,
        lastUpdateTime = bookmark.get("lastUpdateTime")  # : 1701597577000,
        creationTime = bookmark.get("creationTime")  # : 1701597577000,
        order = bookmark.get("order")  # : 65535,
        sid = bookmark.get("sid")  # : "1891657344",
        address = bookmark.get("address")  # : "서울 강남구 남부순환로 2942",
        memo = bookmark.get("memo")  # : null,
        url = bookmark.get("url")  # : null,
        mcid = bookmark.get("mcid")  # : "DINING",
        mcidName = bookmark.get("mcidName")  # : "음식점",
        rcode = bookmark.get("rcode")  # : "09680106",
        cidPath = bookmark.get("cidPath")  # : ["220036", "220048", "1005445"],
        available = bookmark.get("available")  # : true,
        folderMappings = bookmark.get("folderMappings")  # : null,
        placeInfo = bookmark.get("placeInfo")  # : null,
        isIndoor = bookmark.get("isIndoor")  # : true

        print(f"{name} - {address}")
        new_place = Place(
            name=name,
            address=address,
            latitude=py,
            longitude=px,
        )
        places.append(new_place)

    result = Place.objects.bulk_create(objs=places)

    print(f"{len(result)}개의 장소가 추가되었습니다.")

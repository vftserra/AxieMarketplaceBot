import aiohttp

url = "https://axieinfinity.com/graphql-server-v2/graphql"


async def get_floor_price(parts : list):

    payload = {
        "operationName": "GetAxieBriefList",
        "variables": {
            "from": 0,
            "size": 1,
            "sort": "PriceAsc",
            "auctionType": "Sale",
            "criteria": {
                'parts' : parts
            }
        },
        "query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=payload) as res:

            if res.status != 200:
                return False

            resp = await res.json()


    try:
        return round(int(resp['data']['axies']['results'][0]['auction']['currentPrice']) * (10 ** -18), 6)

    except IndexError:
        return "N/A"





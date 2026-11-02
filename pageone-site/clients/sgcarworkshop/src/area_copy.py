"""Area descriptions for estate pages (SEO pass, 2 Nov 2026).

General public knowledge only: MRT stations, malls, parks, hospitals, roads. Nothing here describes a workshop, its services,
prices, hours or quality. slug -> (paragraph, [MRT stations], [landmarks]). Keep every fact checkable on a street map.
"""

AREA_COPY = {
    'kaki-bukit': (
        "Kaki Bukit sits between Bedok and Paya Lebar in the east of Singapore. Kaki Bukit MRT station on the Downtown Line serves the estate, "
        "and Bedok Reservoir and Bedok Reservoir MRT lie a short drive to the east. The area is mostly light industrial, laid out around Kaki Bukit Avenue 1 to 6, "
        "Kaki Bukit Road and Kaki Bukit Industrial Terrace, with trade units, warehouses and car-related businesses sharing the same blocks. "
        "Many drivers come here from the surrounding Bedok, Tampines and Geylang neighbourhoods, and the Pan-Island Expressway and Tampines Expressway are both close, "
        "which makes it easy to reach from most of the east.",
        ['Kaki Bukit', 'Bedok Reservoir', 'Ubi'], ['Kaki Bukit Industrial Estate', 'Bedok Reservoir', 'Kaki Bukit Avenue 1']),
    'ubi': (
        "Ubi is a long-established industrial area next to Paya Lebar, in the Geylang planning area. It is centred on Ubi Avenue 1 to 4, Ubi Road 1 to 4 and Paya Ubi, "
        "and Ubi MRT station on the Downtown Line sits at its heart. Paya Lebar MRT, an interchange between the East West and Circle lines, is a short distance to the south, "
        "and Paya Lebar Quarter and the Singapore Post Centre are the nearest large landmarks. Ubi TechPark and older factory blocks sit beside motor trade units, "
        "so the area has a mix of office workers, delivery vans and private-car owners. The Kallang-Paya Lebar Expressway and Pan-Island Expressway connect it to the rest of the island.",
        ['Ubi', 'Paya Lebar', 'Kaki Bukit'], ['Ubi TechPark', 'Paya Lebar Quarter', 'Ubi Avenue 1']),
    'eunos': (
        "Eunos is a mixed residential and light-industrial area in the Geylang planning area, between Paya Lebar and Bedok. Eunos MRT station on the East West Line serves it, "
        "and Kembangan and Paya Lebar stations are the next stops either side. Eunos Crescent and Eunos Industrial Estate (the Eunos Link and Eunos Avenue roads) hold the trade units, "
        "while Geylang Serai Market and the Joo Chiat Road shophouse belt are a few minutes away. Drivers reach it from Sims Avenue, Changi Road and the Pan-Island Expressway, "
        "and it is close to both Ubi and Kaki Bukit for anyone comparing workshops across the three areas.",
        ['Eunos', 'Kembangan', 'Paya Lebar'], ['Geylang Serai Market', 'Eunos Crescent', 'Sims Avenue']),
    'bedok-north': (
        "Bedok North is in the east of Singapore, around Bedok North Avenue 1 to 4 and Bedok North Street 1 to 5, beside Bedok Reservoir. Bedok North MRT station on the Downtown Line "
        "and Bedok Reservoir MRT station are the closest stations, and Bedok Mall and Bedok Bus Interchange are the nearest large landmarks. The area combines HDB estates with a "
        "pocket of light industry and trade units near Bedok Industrial Park. The Pan-Island Expressway and Tampines Expressway pass close by, so it is an easy drive from "
        "Tampines, Simei, Bedok and Kaki Bukit.",
        ['Bedok North', 'Bedok Reservoir', 'Bedok'], ['Bedok Reservoir', 'Bedok Mall', 'Bedok Industrial Park']),
    'changi-loyang': (
        "Changi and Loyang make up the far east of Singapore, beyond Pasir Ris and Tampines. The area is best known for Changi Airport and Changi Business Park, "
        "with Changi Beach Park and the Changi Village hawker centre on the northern coast. Loyang Way, Loyang Avenue and Loyang Crescent hold an industrial estate of "
        "trade units and warehouses, near the Loyang Offshore Marine Centre. Changi Airport MRT station and Tanah Merah MRT station are the nearest stations, "
        "and the East Coast Parkway runs along the southern edge, so it is a straightforward drive from the east coast and Pasir Ris.",
        ['Changi Airport', 'Tanah Merah', 'Pasir Ris'], ['Changi Airport', 'Changi Business Park', 'Changi Village']),
    'woodlands': (
        "Woodlands is the largest town in the north-west of Singapore, facing Johor Bahru across the Causeway. Woodlands MRT station, which serves both the North South and "
        "Thomson-East Coast lines, is beside Causeway Point and Woodlands Civic Centre, and Woodlands Checkpoint is the main land crossing to Malaysia. "
        "Industrial and trade units are found around Woodlands Industrial Park E and Woodlands Avenue 12, away from the town centre. The Bukit Timah Expressway and Seletar Expressway "
        "connect the area to the city, and Admiralty and Marsiling are the neighbouring districts. Woodlands Waterfront Park sits on the northern shore.",
        ['Woodlands', 'Marsiling', 'Admiralty'], ['Causeway Point', 'Woodlands Checkpoint', 'Woodlands Waterfront Park']),
    'kranji': (
        "Kranji is in the north-west of Singapore, between Woodlands and the Lim Chu Kang farmland. Kranji MRT station on the North South Line is the nearest station, and the "
        "Kranji War Memorial and Kranji Reservoir are the well-known landmarks. The industrial pocket lies around Kranji Way, Kranji Road and Jalan Lam Huat, and extends "
        "towards Sungei Kadut. The Bukit Timah Expressway and Kranji Expressway pass close by, so it connects quickly to Woodlands, Choa Chu Kang and the Second Link crossing "
        "at Tuas for drivers who travel for work.",
        ['Kranji', 'Woodlands', 'Marsiling'], ['Kranji War Memorial', 'Kranji Reservoir', 'Kranji Way']),
    'yishun': (
        "Yishun is a large northern town, with Yishun MRT station on the North South Line beside Northpoint City and the Yishun bus interchange. Khoo Teck Puat Hospital and "
        "Yishun Pond are on the north side of the town, and Lower Seletar Reservoir lies to the east. Yishun has two motor trade clusters: Yishun Industrial Park A and the area "
        "around Yishun Industrial Street 1, near North Spring Bizhub. The Seletar Expressway and Central Expressway link it to Ang Mo Kio and the city, and Sembawang and "
        "Woodlands are the nearest neighbouring areas.",
        ['Yishun', 'Khatib', 'Canberra'], ['Northpoint City', 'Khoo Teck Puat Hospital', 'Yishun Pond']),
    'sembawang-admiralty': (
        "Sembawang and Admiralty are neighbouring areas in the north of Singapore. Admiralty MRT station and Sembawang MRT station are both on the North South Line, and Sun Plaza "
        "and Sembawang Shopping Centre are the local malls. Sembawang Park and Sembawang Hot Spring lie on the northern coast, while Woodlands Waterfront is a short drive "
        "to the west. Sembawang Road, Admiralty Road and Canberra Road are the main routes, joined by the Seletar Expressway and Bukit Timah Expressway. "
        "Yishun and Woodlands are the nearest towns for anyone looking beyond this area.",
        ['Admiralty', 'Sembawang', 'Canberra'], ['Sun Plaza', 'Sembawang Park', 'Woodlands Waterfront']),
    'ang-mo-kio': (
        "Ang Mo Kio is a mature town in the north-east of Singapore. Ang Mo Kio MRT station on the North South Line sits beside AMK Hub, and Mayflower MRT on the "
        "Thomson-East Coast Line serves the western side. Bishan-Ang Mo Kio Park, Ang Mo Kio Town Garden West and Ang Mo Kio Public Library are well-known local spots. "
        "The Ang Mo Kio Industrial Parks along Ang Mo Kio Avenue 3, 5 and 10 hold trade units and workshops away from the housing blocks. The Central Expressway and "
        "Seletar Expressway pass nearby, linking the area with Yishun, Bishan and Serangoon North.",
        ['Ang Mo Kio', 'Mayflower', 'Yio Chu Kang'], ['AMK Hub', 'Bishan-Ang Mo Kio Park', 'Ang Mo Kio Industrial Park']),
    'serangoon-north': (
        "Serangoon North lies in the north-east, between Ang Mo Kio and Hougang. Serangoon MRT station, an interchange between the North East and Circle lines, is the nearest major "
        "station, beside NEX shopping mall and the Serangoon bus interchange. Serangoon North Avenue 1 to 5 and Serangoon North Industrial Estate hold light industrial units, "
        "while Serangoon Garden is a landed residential neighbourhood to the south. The Tampines Expressway and Central Expressway are the main routes, and Ang Mo Kio, "
        "Defu and Bishan are the neighbouring areas.",
        ['Serangoon', 'Lorong Chuan', 'Kovan'], ['NEX', 'Serangoon Garden', 'Serangoon North Avenue 1']),
    'defu-hougang': (
        "Defu and Hougang are in the north-east of Singapore. Defu Industrial Park (Defu Lane and Defu Avenue) is a light industrial pocket near Hougang and Kovan. "
        "Hougang MRT station and Kovan MRT station on the North East Line are the nearest stations, with Hougang Mall and Kovan Hub close to each. "
        "The Tampines Expressway and Kallang-Paya Lebar Expressway connect the area with Serangoon, Sengkang and Paya Lebar. Hougang Stadium and the Punggol and Sengkang "
        "towns lie to the north-east.",
        ['Hougang', 'Kovan', 'Buangkok'], ['Hougang Mall', 'Kovan Hub', 'Defu Lane']),
    'sengkang': (
        "Sengkang is a newer town in the north-east of Singapore, built around the Sengkang town centre. Sengkang MRT station connects the North East Line to the Sengkang LRT "
        "loops, and Compass One mall and Sengkang General Hospital are the main local landmarks. Sengkang Riverside Park and the Sungei Serangoon waterway run through the town. "
        "The Tampines Expressway and Kallang-Paya Lebar Expressway give access to Hougang, Punggol and the rest of the island. Defu and Serangoon North are the closest "
        "areas with industrial units.",
        ['Sengkang', 'Buangkok', 'Rivervale'], ['Compass One', 'Sengkang General Hospital', 'Sengkang Riverside Park']),
    'sin-ming-bishan': (
        "Sin Ming and Bishan lie in the centre-north of Singapore. Sin Ming Industrial Estate, around Sin Ming Road, Sin Ming Lane and is a long-running motor "
        "trade area, while Bishan town has Junction 8 and Bishan MRT station, an interchange between the North South and Circle lines. Bishan-Ang Mo Kio Park is a large "
        "green space nearby, and Thomson Road and the Central Expressway are the main routes. Toa Payoh and Ang Mo Kio are the neighbouring areas for anyone looking a little further out.",
        ['Bishan', 'Marymount', 'Caldecott'], ['Junction 8', 'Bishan-Ang Mo Kio Park', 'Sin Ming Road']),
    'toa-payoh': (
        "Toa Payoh is one of Singapore's oldest HDB towns, in the central region. Toa Payoh MRT station on the North South Line sits beside HDB Hub and Toa Payoh Central, "
        "and Braddell MRT lies to the north. Toa Payoh Industrial Park and the Toa Payoh Lorong 8 area hold light industrial units and trade premises. "
        "The Central Expressway and Pan-Island Expressway run along the edges of the town, so the area is quick to reach from Bishan, Novena and MacPherson.",
        ['Toa Payoh', 'Braddell', 'Bishan'], ['HDB Hub', 'Toa Payoh Central', 'Toa Payoh Lorong 8']),
    'macpherson': (
        "MacPherson is in the central region, between Paya Lebar and Toa Payoh. MacPherson MRT station, an interchange between the Circle and Downtown lines, is the nearest station, "
        "with Paya Lebar MRT to the east. The area is centred on MacPherson Road, Circuit Road and Pine Close, with a mix of HDB blocks, shophouses and light industrial units. "
        "The Pan-Island Expressway and Kallang-Paya Lebar Expressway pass close by, so it is an easy drive from Ubi, Geylang and Toa Payoh.",
        ['MacPherson', 'Paya Lebar', 'Potong Pasir'], ['MacPherson Road', 'Circuit Road', 'Paya Lebar Quarter']),
    'jalan-besar-kallang-bahru': (
        "Jalan Besar and Kallang Bahru are close to the city centre. Jalan Besar MRT station on the Downtown Line and Lavender MRT station on the East West Line serve the area, "
        "and Farrer Park is nearby. Jalan Besar is known for its shophouses and the Jalan Besar Stadium, while Kallang Bahru and Kallang Basin are close to the Singapore Sports Hub "
        "and the National Stadium. The Pan-Island Expressway and Kallang-Paya Lebar Expressway connect the area to the east and north of the island.",
        ['Jalan Besar', 'Lavender', 'Boon Keng'], ['Jalan Besar Stadium', 'Singapore Sports Hub', 'Kallang Basin']),
    'alexandra-bukit-merah': (
        "Alexandra and Bukit Merah are in the south-west of the central region. Redhill MRT station and Queenstown MRT station on the East West Line serve the area, with Tiong Bahru MRT "
        "close by. Alexandra Road is home to Alexandra Hospital and the IKEA Alexandra store, and Henderson Road and Bukit Merah Central hold the local HDB estates and shops. "
        "The Ayer Rajah Expressway and Central Expressway link the area with the city and the west, and Telok Blangah is the next district to the south.",
        ['Redhill', 'Queenstown', 'Tiong Bahru'], ['Alexandra Hospital', 'IKEA Alexandra', 'Henderson Road']),
    'toh-guan-jurong-east': (
        "Toh Guan and Jurong East are in the west of Singapore. Jurong East MRT station, an interchange for the North South and East West lines, sits beside JEM, Westgate and IMM, "
        "and the Chinese Garden and Science Centre Singapore are nearby. Toh Guan Road and the Toh Guan industrial estate hold trade units, warehouses and car-related businesses. "
        "The Ayer Rajah Expressway and Pan-Island Expressway pass close by, so the area is easy to reach from Clementi, Bukit Batok and Jurong West.",
        ['Jurong East', 'Chinese Garden', 'Clementi'], ['JEM', 'Westgate', 'Science Centre Singapore']),
    'jurong-west': (
        "Jurong West is a large residential and industrial area in the west. Boon Lay MRT station and Pioneer MRT station on the East West Line serve it, and Jurong Point is the main "
        "shopping mall, beside the Boon Lay bus interchange. Nanyang Technological University lies to the west, and Jurong Lake and the Jurong Industrial Estate are to the east. "
        "The Pan-Island Expressway and Ayer Rajah Expressway link it with the city, and Tuas and Jurong East are the nearest neighbouring areas.",
        ['Boon Lay', 'Pioneer', 'Lakeside'], ['Jurong Point', 'Nanyang Technological University', 'Jurong Lake']),
    'pandan-loop': (
        "Pandan Loop is a small industrial area in the south-west, near Pandan Reservoir and Clementi. Clementi MRT station on the East West Line is the nearest station, "
        "with Clementi Mall and West Coast Park nearby. Pandan Loop and the roads around it hold light industrial units and trade premises. The Ayer Rajah Expressway and "
        "West Coast Highway pass close by, and Jurong East and Bukit Batok are the neighbouring areas.",
        ['Clementi', 'Dover', 'Jurong East'], ['Pandan Reservoir', 'Clementi Mall', 'West Coast Park']),
    'bukit-batok': (
        "Bukit Batok is a town in the west of Singapore. Bukit Batok MRT station on the North South Line sits beside West Mall, and Bukit Gombak and Jurong East stations are the "
        "next stops either side. Bukit Batok Nature Park and Little Guilin are popular green spaces, while Bukit Batok Industrial Park A holds light industrial units. "
        "The Pan-Island Expressway and Bukit Timah Expressway connect it to Choa Chu Kang, Jurong East and the city.",
        ['Bukit Batok', 'Bukit Gombak', 'Jurong East'], ['West Mall', 'Bukit Batok Nature Park', 'Little Guilin']),
    'tuas': (
        "Tuas is the industrial far west of Singapore. Tuas Link MRT station on the East West Line is the western end of the line, and Tuas West Road and Tuas Avenue run through "
        "the factory and warehouse estates. Tuas Mega Port and the Tuas Checkpoint at the Second Link to Malaysia are the well-known landmarks, and the Ayer Rajah Expressway "
        "and Pan-Island Expressway are the main routes from the rest of the island. Jurong West is the nearest residential area.",
        ['Tuas Link', 'Tuas West Road', 'Tuas Crescent'], ['Tuas Mega Port', 'Tuas Checkpoint', 'Tuas Avenue']),
}

# Plain-English region notes used on region pages (general public knowledge).
REGION_COPY = {
    'north': "The North region covers the towns along the Causeway and the Straits of Johor: Woodlands, Kranji, Yishun, Sembawang and Admiralty. The North South Line runs the length of it, from Yishun to Woodlands, and the Seletar Expressway and Bukit Timah Expressway are the main roads.",
    'north-east': "The North-East region covers Ang Mo Kio, Serangoon North, Hougang, Defu and Sengkang. The North East Line and the Tampines, Central and Kallang-Paya Lebar expressways connect these towns with the city and Punggol.",
    'east': "The East region covers Kaki Bukit, Bedok North, Changi and Loyang. The Downtown Line serves Kaki Bukit and Bedok North, the East Coast Parkway runs along the coast, and Changi Airport is at the eastern tip.",
    'west': "The West region covers Jurong East, Toh Guan, Jurong West, Pandan Loop, Bukit Batok and Tuas. The East West Line and North South Line serve the area, and the Ayer Rajah and Pan-Island expressways are the main routes.",
    'central': "The Central region covers Sin Ming, Bishan, Toa Payoh, Ubi, Eunos, MacPherson, Jalan Besar, Kallang Bahru, Alexandra and Bukit Merah. It is the well-connected part of the island, with the North South, East West, Circle and Downtown lines all passing through.",
    'mobile': "Mobile services have no single shopfront. The provider comes to the place where your car is parked, for example a home carpark or an office, so the listings here are not tied to one area.",
}

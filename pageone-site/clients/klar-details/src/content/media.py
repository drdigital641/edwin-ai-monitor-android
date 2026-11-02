"""Klar Details existing-media catalogue (URLs verbatim from klardetails.com.sg, fetched 2026-11-01)."""
U = 'https://klardetails.com.sg/wp-content/uploads/'

IMAGES = {
    # HERO: real workshop/car photos (landscape)
    'bmw_infrared': {'url': U + '2026/10/BMW-Infrared-Paint-Curing-1024x815.jpg', 'alt': 'Black BMW under infrared curing lamps', 'use': 'HERO'},
    'bmw_infrared_full': {'url': U + '2026/10/BMW-Infrared-Paint-Curing.jpg', 'alt': 'Black BMW under infrared curing lamps', 'use': 'HERO'},
    'bmw_m6': {'url': U + '2026/10/BMW-M6-Professional-Car-Care.jpg', 'alt': 'BMW M6 professional car care', 'use': 'HERO'},
    'coating_black_hood': {'url': U + '2026/10/Professional-Car-Ceramic-Coating-1.jpg', 'alt': 'Technician applying coating to black car hood', 'use': 'HERO'},
    'ceramic_gray_car': {'url': U + '2026/10/Professional-Ceramic-Car-Coating-1024x735.jpeg', 'alt': 'Technician applying ceramic coating to gray car', 'use': 'HERO'},
    'porsche_emblem': {'url': U + '2026/10/Porsche-Car-Emblem.jpg', 'alt': 'Porsche emblem on dark car hood', 'use': 'HERO'},
    # GALLERY: "our works" real job photos
    'tesla_byd': {'url': U + '2025/07/TESLA-AND-BYD-1.jpeg', 'alt': 'Tesla and BYD after coating', 'use': 'GALLERY'},
    'lexus_rc': {'url': U + '2022/10/Ceramic-Coating-on-Lexus-RC.jpg', 'alt': 'Ceramic coating on Lexus RC', 'use': 'GALLERY'},
    'infrared_curing_2': {'url': U + '2022/10/coating-infrared-curing-2.jpg', 'alt': 'Coating infrared curing', 'use': 'GALLERY'},
    'bespoke_dubai': {'url': U + '2022/06/KlarBespoke-in-Dubai-L.jpg', 'alt': 'KlarBespoke in Dubai', 'use': 'GALLERY'},
    'r8_titanium': {'url': U + '2022/10/Titanium-Coating-R8.jpg', 'alt': 'Titanium coating on Audi R8', 'use': 'GALLERY'},
    'graphene_coating': {'url': U + '2022/07/graphene-coating-klar-details.jpg', 'alt': 'Graphene coating by Klar Details', 'use': 'GALLERY'},
    'tesla_charging': {'url': U + '2025/07/tesla-charging-1.jpeg', 'alt': 'Tesla charging after detailing', 'use': 'GALLERY'},
    'rolls_diamond': {'url': U + '2022/10/Diamond-Coat-rolls-royce.jpeg', 'alt': 'Diamond coat on Rolls-Royce', 'use': 'GALLERY'},
    'byd': {'url': U + '2025/07/BYD-1.jpeg', 'alt': 'BYD detailed by Klar Details', 'use': 'GALLERY'},
    'byd_2': {'url': U + '2025/07/BYD2-1.jpeg', 'alt': 'BYD detailed by Klar Details', 'use': 'GALLERY'},
    'diamond_coating': {'url': U + '2022/07/diamond-coating-klar-details.jpg', 'alt': 'Diamond coating by Klar Details', 'use': 'GALLERY'},
    'interior_1': {'url': U + '2022/06/Interior-Services-1.png', 'alt': 'Interior detailing service', 'use': 'GALLERY'},
    'service_ext_hero': {'url': U + '2026/05/WhatsApp-Image-2026-05-22-at-5.00.30-PM-e1779469364901.jpeg', 'alt': 'Exterior service', 'use': 'GALLERY'},
    'service_int_hero': {'url': U + '2026/05/WhatsApp-Image-2026-05-23-at-7.43.29-PM.jpeg', 'alt': 'Interior service', 'use': 'GALLERY'},
    'service_maint_hero': {'url': U + '2026/05/WhatsApp-Image-2026-05-23-at-7.45.19-PM.jpeg', 'alt': 'Maintenance service', 'use': 'GALLERY'},
    'graphene_trial_photo': {'url': U + '2026/05/WhatsApp-Image-2026-05-22-at-4.47.38-PM-1.jpeg', 'alt': 'Graphene coating trial', 'use': 'GALLERY'},
    # BRAND
    'signage': {'url': U + '2026/10/Klar-Details-Illuminated-Signage-1024x681.png', 'alt': 'Klar Details illuminated business sign', 'use': 'BRAND'},
    'signage_full': {'url': U + '2026/10/Klar-Details-Illuminated-Signage.png', 'alt': 'Klar Details illuminated business sign', 'use': 'BRAND'},
    'bottles': {'url': U + '2026/10/Klarcoat-Nanotechnology-Surface-Treatments-1024x546.jpeg', 'alt': 'Klarcoat nanotechnology surface treatment bottles', 'use': 'BRAND'},
    'bottles_full': {'url': U + '2026/10/Klarcoat-Nanotechnology-Surface-Treatments.jpeg', 'alt': 'Klarcoat nanotechnology surface treatment bottles', 'use': 'BRAND'},
    'products': {'url': U + '2026/10/Klar-Coat-Car-Care-Products.jpg', 'alt': 'Klar Coat car care products', 'use': 'BRAND'},
    'polo': {'url': U + '2026/10/Klar-Specialist-Branded-Polo-Shirt-1024x574.jpg', 'alt': 'Klar Specialist black polo shirt with red trim', 'use': 'BRAND'},
    'business_cards': {'url': U + '2026/10/Klar-Details-Business-Cards.jpg', 'alt': 'Klar Details business cards', 'use': 'BRAND'},
    'wall_display': {'url': U + '2026/10/Klar-Details-Car-Detailing-Brand-1.png', 'alt': 'Klar Details car detailing wall display', 'use': 'BRAND'},
    'graphene_flyer': {'url': U + '2026/10/88-Graphene-Car-Bonnet-Coating.jpeg', 'alt': 'Klardetails $88 graphene car bonnet coating flyer', 'use': 'BRAND'},
    'logo_red_k': {'url': U + '2026/10/Klar-Details-Logo.png', 'alt': 'Klar Details logo with red K', 'use': 'BRAND'},
    'logo_klaredit': {'url': U + '2022/09/klaredit-removebg-preview.png', 'alt': 'Klar Details', 'use': 'BRAND'},
    'logo_footer_mk': {'url': U + '2022/09/WhatsApp_Image_2026-05-24_at_5.43.09_PM-removebg-preview-e1779637194432.png', 'alt': 'Klar Details', 'use': 'BRAND'},
    'logo_oie': {'url': U + '2022/06/oie_transparent.png', 'alt': 'Klar Details', 'use': 'BRAND'},
}

VIDEOS = [
    {'url': U + '2022/10/Video-for-Klar.mp4', 'poster_key': 'bmw_infrared',
     'note': 'Linked as plain link under "Book Appointment" on home page; no <video> element or YouTube/Vimeo embed on any page. Site links to YouTube and TikTok channels only.'},
]

LOGO = U + '2026/10/Klar-Details-Logo.png'

# Search returned no listing near Toh Guan Rd East (OpenSEO search_local_businesses, 2026-11-01); not verified.
GBP = None

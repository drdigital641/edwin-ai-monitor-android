"""Fluid and plug specs per car model (indicative, from general knowledge; Autotex confirms by chassis number).
key: (engine oil litres, oil grade, cylinders, gearbox group, gearbox text, gearbox fluid litres)
gearbox group: SP3 / SP4 / SP6 (hydraulic automatics), DCT (dual clutch), CVT (belt/IVT)."""
SPECS = {
 "optima-jf":    (4.0, "0W-20", 4, "SP4", "6-speed automatic", 7.3),
 "carens-rp":    (3.6, "5W-30", 4, "SP4", "6-speed automatic", 7.0),
 "niro-de":      (3.6, "0W-20", 4, "DCT", "6-speed dual clutch (hybrid)", 1.7),
 "sorento-um":   (4.8, "5W-30", 4, "SP4", "6-speed automatic", 7.3),
 "sorento-mq4":  (4.8, "0W-30", 4, "DCT", "8-speed dual clutch", 7.0),
 "sportage-nq5": (4.8, "0W-30", 4, "DCT", "7-speed dual clutch", 1.9),
 "sportage-ql":  (4.0, "5W-20", 4, "SP4", "6-speed automatic", 7.3),
 "picanto-ja":   (3.0, "0W-20", 3, "SP3", "4-speed automatic", 6.0),
 "picanto-ta":   (3.3, "5W-30", 3, "SP3", "4-speed automatic", 6.0),
 "cerato-bd":    (3.6, "0W-20", 4, "SP4", "6-speed automatic", 7.0),
 "cerato-yd":    (3.6, "5W-30", 4, "SP4", "6-speed automatic", 7.0),
 "rio-yb":       (3.3, "0W-20", 4, "SP4", "6-speed automatic", 7.0),
 "seltos-sp2":   (4.8, "0W-30", 4, "DCT", "7-speed dual clutch", 1.9),
 "stonic-yb":    (3.5, "0W-30", 3, "DCT", "7-speed dual clutch", 1.7),
 "k5-dl3":       (4.0, "0W-20", 4, "SP6", "8-speed automatic", 7.8),
 "carnival-ka4": (5.8, "0W-30", 6, "SP6", "8-speed automatic", 8.2),
 "carnival-yp":  (5.7, "5W-30", 6, "SP4", "6-speed automatic", 7.8),
 "stinger-ck":   (5.0, "5W-30", 4, "SP6", "8-speed automatic", 8.0),
 "starex-tq":    (7.0, "5W-30", 4, "SP3", "5-speed automatic", 8.0),
 "santa-fe-tm":  (4.8, "5W-30", 4, "SP4", "6-speed automatic", 7.3),
 "santa-fe-dm":  (4.8, "5W-30", 4, "SP4", "6-speed automatic", 7.3),
 "santa-fe-mx5": (4.0, "0W-20", 4, "SP4", "6-speed automatic (hybrid)", 7.5),
 "tucson-nx4":   (4.8, "0W-30", 4, "DCT", "7-speed dual clutch", 2.0),
 "tucson-tl":    (4.0, "5W-30", 4, "DCT", "7-speed dual clutch", 1.8),
 "kona-os":      (4.0, "5W-30", 4, "DCT", "7-speed dual clutch", 1.8),
 "kona-sx2":     (4.0, "0W-20", 4, "CVT", "intelligent variable (IVT)", 6.5),
 "ioniq-ae":     (3.6, "0W-20", 4, "DCT", "6-speed dual clutch (hybrid)", 1.7),
 "i30-pd":       (4.0, "5W-30", 4, "DCT", "7-speed dual clutch", 1.8),
 "i30-n":        (5.3, "5W-30", 4, "DCT", "8-speed wet dual clutch", 7.0),
 "avante-n":     (5.3, "5W-30", 4, "DCT", "8-speed wet dual clutch", 7.0),
 "avante-cn7":   (3.8, "0W-20", 4, "CVT", "intelligent variable (IVT)", 7.0),
 "avante-ad":    (3.6, "5W-30", 4, "SP4", "6-speed automatic", 7.0),
 "i40-vf":       (4.5, "5W-30", 4, "SP4", "6-speed automatic", 7.3),
 "sonata-dn8":   (4.2, "0W-20", 4, "SP4", "6-speed automatic", 7.3),
 "sonata-lf":    (4.0, "5W-20", 4, "SP4", "6-speed automatic", 7.3),
 "staria-us4":   (7.6, "5W-30", 4, "SP6", "8-speed automatic", 9.0),
 "niro-sg2":     (3.6, "0W-20", 4, "DCT", "6-speed dual clutch (hybrid)", 1.7),
 "veloster-fs":  (4.0, "5W-30", 4, "DCT", "7-speed dual clutch", 1.8),
 "venue-qx":     (3.5, "0W-30", 3, "DCT", "7-speed dual clutch", 1.8),
 "accent-rb":    (3.6, "5W-30", 4, "SP3", "4-speed automatic", 6.0),
}
GB_LABEL = {"SP3": "ATF SP3", "SP4": "ATF SP4", "SP6": "ATF SP6 (8-speed)", "DCT": "DCT fluid", "CVT": "CVT fluid"}
GB_FACTOR = {"SP3": 1.0, "SP4": 1.1, "SP6": 1.35, "CVT": 1.45, "DCT": 1.6}  # price factor on the 4 L ATF base price

def spec(key):
    s = SPECS.get(key)
    if not s: return None
    return dict(oil_l=s[0], grade=s[1], cyl=s[2], gb=s[3], gbtext=s[4], fluid_l=s[5])

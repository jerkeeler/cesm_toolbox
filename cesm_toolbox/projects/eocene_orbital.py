"""

"""
from ..proxy_data import ProxyData, ProxySource, ProxyLocality

# def load_cam_data():
#     orb_modern_3x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM03xx2.01/b.e12.B1850C5CN.f19_g16.iPETM03xx2.01.cam.h0.0350-0399.climo.nc")
#     orb_maxN_3x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM03x.OrbMaxN.01/b.e12.B1850C5CN.f19_g16.iPETM03x.OrbMaxN.01.cam.h0.2601-2700.climo.nc")
#     orb_maxS_3x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM03x.OrbMaxS.01/b.e12.B1850C5CN.f19_g16.iPETM03x.OrbMaxS.01.cam.h0.2601-2700.climo.nc")
#     orb_min_3x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM03x.OrbMin.01/b.e12.B1850C5CN.f19_g16.iPETM03x.OrbMin.01.cam.h0.2601-2700.climo.nc")
#
#     orb_modern_6x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM06x.09/b.e12.B1850C5CN.f19_g16.iPETM06x.09.cam.h0.2101-2200.climo.nc")
#     orb_maxN_6x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM06x.OrbMaxN.01/b.e12.B1850C5CN.f19_g16.iPETM06x.OrbMaxN.01.cam.h0.2601-2700.climo.nc")
#     orb_maxS_6x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM06x.OrbMaxS.01/b.e12.B1850C5CN.f19_g16.iPETM06x.OrbMaxS.01.cam.h0.2601-2700.climo.nc")
#     orb_min_6x = read_cam_data(f"{DATA_PATH}/b.e12.B1850C5CN.f19_g16.iPETM06x.OrbMin.01/b.e12.B1850C5CN.f19_g16.iPETM06x.OrbMin.01.cam.h0.2601-2700.climo.nc")

PROXY_DATA = [
    ProxyData(
        lon=-4.75,
        lat=32.25,
        d18o=-1.76,
        d18o_std=0.11,
        sst=20.74,
        sst_std=0.52,
        glassy=False,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="Alamedilla",
    ),
    ProxyData(
        lon=--55.55,
        lat=38.45,
        d18o=-3.44,
        d18o_std=0.5,
        sst=28.16,
        sst_std=2.57,
        glassy=True,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="Bass River",
    ),
    ProxyData(
        lon=-173.95,
        lat=-62.45,
        d18o=-2.41,
        d18o_std=0.39,
        sst=20.54,
        sst_std=1.87,
        glassy=False,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="DSDP 277",
    ),
    ProxyData(
        lon=-10.95,
        lat=41.95,
        d18o=-2.24,
        d18o_std=0.39,
        sst=22.13,
        sst_std=1.87,
        glassy=True,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="DSDP 401",
    ),
    ProxyData(
        lon=-7.75,
        lat=-34.95,
        d18o=-1.46,
        d18o_std=0.13,
        sst=19.74,
        sst_std=0.63,
        glassy=False,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="DSDP 527",
    ),
    ProxyData(
        lon=-15.65,
        lat=43.75,
        d18o=-2.39,
        d18o_std=0.38,
        sst=22.36,
        sst_std=1.89,
        glassy=False,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="DSDP 549",
    ),
    ProxyData(
        lon=-103.75,
        lat=42.25,
        d18o=-2.88,
        d18o_std=0.24,
        sst=22.02,
        sst_std=1.15,
        glassy=True,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="Lodo Gulch",
    ),
    ProxyData(
        lon=-56.75,
        lat=37.65,
        d18o=-3.51,
        d18o_std=0.41,
        sst=28.5,
        sst_std=2.12,
        glassy=True,
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
        name="Millville",
    ),
    ProxyData(
        lon=0.55,
        lat=-64.0,
        d18o=-1.52,
        d18o_std=0.06,
        sst=16.49,
        sst_std=0.28,
        glassy=False,
        name="ODP 689",
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
    ),
    ProxyData(
        lon=-1.35,
        lat=-65.05,
        d18o=-1.83,
        d18o_std=0.53,
        sst=17.96,
        sst_std=2.52,
        glassy=False,
        name="ODP 690B",
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
    ),
    ProxyData(
        lon=-143.85,
        lat=4.85,
        d18o=-3.82,
        d18o_std=0.41,
        sst=31.07,
        sst_std=2.11,
        glassy=False,
        name="ODP 865",
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
    ),
    ProxyData(
        lon=-161.45,
        lat=22.2,
        d18o=-1.77,
        d18o_std=0.25,
        sst=20.78,
        sst_std=1.22,
        glassy=False,
        name="ODP 1209",
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
    ),
    ProxyData(
        lon=34.15,
        lat=-18.65,
        d18o=-3.44,
        d18o_std=0.35,
        sst=30.15,
        sst_std=1.81,
        glassy=True,
        name="Tanzania TDP14",
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
    ),
    ProxyData(
        lon=-102.8,
        lat=41.15,
        d18o=-3.21,
        d18o_std=0.12,
        sst=23.67,
        sst_std=0.59,
        glassy=True,
        name="Tumey Gulch",
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
    ),
    ProxyData(
        lon=-56.45,
        lat=38.65,
        d18o=-3.63,
        d18o_std=0.29,
        sst=29.07,
        sst_std=1.47,
        glassy=True,
        name="Wilson Lake",
        source=ProxySource.jiang_2020,
        locality=ProxyLocality.marine,
    ),
]

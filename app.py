import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import concurrent.futures
import warnings
import requests
import time

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="TradingView Pro - Indian Stock Screener",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Professional Indian Stock Market Screener"}
)

# Load CSS
def load_css():
    try:
        with open("style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("style.css file not found. Please ensure it's in the same directory.")

load_css()

# COMPREHENSIVE INDIAN STOCK DATABASE
@st.cache_data(ttl=3600, show_spinner=False)
def get_all_indian_stocks():
    """Complete Indian Stock Database - All NSE & BSE Listed Stocks"""
    return {
        'nse_large_cap': {
            # NIFTY 50 - Complete
            "RELIANCE.NS": "Reliance Industries Limited", "TCS.NS": "Tata Consultancy Services Limited",
            "HDFCBANK.NS": "HDFC Bank Limited", "INFY.NS": "Infosys Limited", "HINDUNILVR.NS": "Hindustan Unilever Limited",
            "ICICIBANK.NS": "ICICI Bank Limited", "KOTAKBANK.NS": "Kotak Mahindra Bank Limited", "SBIN.NS": "State Bank of India",
            "BHARTIARTL.NS": "Bharti Airtel Limited", "ITC.NS": "ITC Limited", "ASIANPAINT.NS": "Asian Paints Limited",
            "LT.NS": "Larsen & Toubro Limited", "AXISBANK.NS": "Axis Bank Limited", "MARUTI.NS": "Maruti Suzuki India Limited",
            "SUNPHARMA.NS": "Sun Pharmaceutical Industries Limited", "WIPRO.NS": "Wipro Limited", "ULTRACEMCO.NS": "UltraTech Cement Limited",
            "TITAN.NS": "Titan Company Limited", "HCLTECH.NS": "HCL Technologies Limited", "ONGC.NS": "Oil and Natural Gas Corporation Limited",
            "BAJFINANCE.NS": "Bajaj Finance Limited", "M&M.NS": "Mahindra & Mahindra Limited", "POWERGRID.NS": "Power Grid Corporation of India Limited",
            "NTPC.NS": "NTPC Limited", "JSWSTEEL.NS": "JSW Steel Limited", "TATASTEEL.NS": "Tata Steel Limited",
            "TECHM.NS": "Tech Mahindra Limited", "NESTLEIND.NS": "Nestle India Limited", "COALINDIA.NS": "Coal India Limited",
            "BAJAJFINSV.NS": "Bajaj Finserv Limited", "ADANIENT.NS": "Adani Enterprises Limited", "HDFCLIFE.NS": "HDFC Life Insurance Company Limited",
            "SBILIFE.NS": "SBI Life Insurance Company Limited", "BPCL.NS": "Bharat Petroleum Corporation Limited", "GRASIM.NS": "Grasim Industries Limited",
            "TATAMOTORS.NS": "Tata Motors Limited", "INDUSINDBK.NS": "IndusInd Bank Limited", "CIPLA.NS": "Cipla Limited",
            "EICHERMOT.NS": "Eicher Motors Limited", "IOC.NS": "Indian Oil Corporation Limited", "DIVISLAB.NS": "Divi's Laboratories Limited",
            "BRITANNIA.NS": "Britannia Industries Limited", "APOLLOHOSP.NS": "Apollo Hospitals Enterprise Limited", "DRREDDY.NS": "Dr. Reddy's Laboratories Limited",
            "BAJAJ-AUTO.NS": "Bajaj Auto Limited", "HEROMOTOCO.NS": "Hero MotoCorp Limited", "SHREECEM.NS": "Shree Cement Limited"
        },
        
        'nse_mid_cap': {
            # NIFTY NEXT 50 + Popular Mid Caps
            "ADANIPORTS.NS": "Adani Ports and Special Economic Zone Limited", "BANDHANBNK.NS": "Bandhan Bank Limited",
            "BERGEPAINT.NS": "Berger Paints India Limited", "BIOCON.NS": "Biocon Limited", "BOSCHLTD.NS": "Bosch Limited",
            "COLPAL.NS": "Colgate Palmolive (India) Limited", "CONCOR.NS": "Container Corporation of India Limited",
            "DABUR.NS": "Dabur India Limited", "DLF.NS": "DLF Limited", "GODREJCP.NS": "Godrej Consumer Products Limited",
            "HAVELLS.NS": "Havells India Limited", "HINDALCO.NS": "Hindalco Industries Limited", "HINDPETRO.NS": "Hindustan Petroleum Corporation Limited",
            "ICICIPRULI.NS": "ICICI Prudential Life Insurance Company Limited", "INDUSTOWER.NS": "Indus Towers Limited",
            "JINDALSTEL.NS": "Jindal Steel & Power Limited", "LUPIN.NS": "Lupin Limited", "MARICO.NS": "Marico Limited",
            "MOTHERSON.NS": "Motherson Sumi Systems Limited", "MUTHOOTFIN.NS": "Muthoot Finance Limited", "NMDC.NS": "NMDC Limited",
            "NYKAA.NS": "FSN E-Commerce Ventures Limited", "PAGEIND.NS": "Page Industries Limited", "PEL.NS": "Piramal Enterprises Limited",
            "PIDILITIND.NS": "Pidilite Industries Limited", "PIIND.NS": "PI Industries Limited", "PNB.NS": "Punjab National Bank",
            "PGHH.NS": "Procter & Gamble Hygiene and Health Care Limited", "SIEMENS.NS": "Siemens Limited",
            "TORNTPHARM.NS": "Torrent Pharmaceuticals Limited", "TRENT.NS": "Trent Limited", "VEDL.NS": "Vedanta Limited",
            "VOLTAS.NS": "Voltas Limited", "ZEEL.NS": "Zee Entertainment Enterprises Limited", "AUROPHARMA.NS": "Aurobindo Pharma Limited",
            "BATAINDIA.NS": "Bata India Limited", "CADILAHC.NS": "Cadila Healthcare Limited", "CANBK.NS": "Canara Bank",
            "CHOLAFIN.NS": "Cholamandalam Investment and Finance Company Limited", "CROMPTON.NS": "Crompton Greaves Consumer Electricals Limited",
            "CUMMINSIND.NS": "Cummins India Limited", "DIXON.NS": "Dixon Technologies (India) Limited", "FEDERALBNK.NS": "The Federal Bank Limited",
            "GAIL.NS": "GAIL (India) Limited", "GMRINFRA.NS": "GMR Infrastructure Limited", "GODREJPROP.NS": "Godrej Properties Limited",
            "HDFCAMC.NS": "HDFC Asset Management Company Limited", "IBULHSGFIN.NS": "Indiabulls Housing Finance Limited",
            "IDFCFIRSTB.NS": "IDFC First Bank Limited", "IGL.NS": "Indraprastha Gas Limited", "INDHOTEL.NS": "The Indian Hotels Company Limited",
            "IRCTC.NS": "Indian Railway Catering and Tourism Corporation Limited", "JUBLFOOD.NS": "Jubilant FoodWorks Limited",
            "LICHSGFIN.NS": "LIC Housing Finance Limited", "MCDOWELL-N.NS": "United Spirits Limited", "MINDTREE.NS": "Mindtree Limited",
            "MPHASIS.NS": "MphasisLimited", "MRF.NS": "MRF Limited", "OBEROIRLTY.NS": "Oberoi Realty Limited",
            "OFSS.NS": "Oracle Financial Services Software Limited", "PETRONET.NS": "Petronet LNG Limited", "PFIZER.NS": "Pfizer Limited",
            "PHOENIXMILLS.NS": "The Phoenix Mills Limited", "POLYCAB.NS": "Polycab India Limited", "PVR.NS": "PVR Limited",
            "RBLBANK.NS": "RBL Bank Limited", "RECLTD.NS": "REC Limited", "SAIL.NS": "Steel Authority of India Limited",
            "SRF.NS": "SRF Limited", "SUNTV.NS": "Sun TV Network Limited", "TATACOMM.NS": "Tata Communications Limited",
            "TATACONSUM.NS": "Tata Consumer Products Limited", "TATACHEM.NS": "Tata Chemicals Limited", "TATAPOWER.NS": "Tata Power Company Limited",
            "TORNTPOWER.NS": "Torrent Power Limited", "TV18BRDCST.NS": "TV18 Broadcast Limited", "UBL.NS": "United Breweries Limited",
            "UPL.NS": "UPL Limited", "WHIRLPOOL.NS": "Whirlpool of India Limited", "YESBANK.NS": "Yes Bank Limited",
            "ZYDUSLIFE.NS": "Zydus Lifesciences Limited"
        },
        
        'nse_small_cap': {
            # Additional Popular Small & Mid Cap NSE Stocks
            "360ONE.NS": "360 ONE WAM Limited", "ABCAPITAL.NS": "Aditya Birla Capital Limited", "ABFRL.NS": "Aditya Birla Fashion and Retail Limited",
            "ACC.NS": "ACC Limited", "ADANIGREEN.NS": "Adani Green Energy Limited", "ADANIPOWER.NS": "Adani Power Limited",
            "ADANITRANS.NS": "Adani Transmission Limited", "ALKEM.NS": "Alkem Laboratories Limited", "AMBUJACEM.NS": "Ambuja Cements Limited",
            "APOLLOTYRE.NS": "Apollo Tyres Limited", "ASHOKLEY.NS": "Ashok Leyland Limited", "ASTRAL.NS": "Astral Limited",
            "ATUL.NS": "Atul Limited", "AUBANK.NS": "AU Small Finance Bank Limited", "BALKRISIND.NS": "Balkrishna Industries Limited",
            "BALRAMCHIN.NS": "Balrampur Chini Mills Limited", "BANKBARODA.NS": "Bank of Baroda", "BANKINDIA.NS": "Bank of India",
            "BEL.NS": "Bharat Electronics Limited", "BHARATFORG.NS": "Bharat Forge Limited", "BHEL.NS": "Bharat Heavy Electricals Limited",
            "BLUEDART.NS": "Blue Dart Express Limited", "BSE.NS": "BSE Limited", "CANFINHOME.NS": "Can Fin Homes Limited",
            "CDSL.NS": "Central Depository Services (India) Limited", "CHAMBLFERT.NS": "Chambal Fertilisers and Chemicals Limited",
            "COFORGE.NS": "Coforge Limited", "COROMANDEL.NS": "Coromandel International Limited", "CREDITACCESS.NS": "Creditaccess Grameen Limited",
            "CRISIL.NS": "CRISIL Limited", "DEEPAKNTR.NS": "Deepak Nitrite Limited", "DELTACORP.NS": "Delta Corp Limited",
            "DMART.NS": "Avenue Supermarts Limited", "ESCORTS.NS": "Escorts Limited", "EXIDEIND.NS": "Exide Industries Limited",
            "FSL.NS": "Firstsource Solutions Limited", "GLENMARK.NS": "Glenmark Pharmaceuticals Limited", "GNFC.NS": "Gujarat Narmada Valley Fertilizers and Chemicals Limited",
            "GODREJAGRO.NS": "Godrej Agrovet Limited", "GRANULES.NS": "Granules India Limited", "GRAPHITE.NS": "Graphite India Limited",
            "GUJGASLTD.NS": "Gujarat Gas Limited", "HATSUN.NS": "Hatsun Agro Product Limited", "HONAUT.NS": "Honeywell Automation India Limited",
            "IBREALEST.NS": "Indiabulls Real Estate Limited", "IDBI.NS": "IDBI Bank Limited", "IDFC.NS": "IDFC Limited",
            "IFBIND.NS": "IFB Industries Limited", "IIFL.NS": "India Infradebt Limited", "INDIANB.NS": "Indian Bank",
            "INDIAMART.NS": "IndiaMART InterMESH Limited", "INTELLECT.NS": "Intellect Design Arena Limited", "IPCALAB.NS": "IPCA Laboratories Limited",
            "IRB.NS": "IRB Infrastructure Developers Limited", "ISEC.NS": "ICICI Securities Limited", "JBCHEPHARM.NS": "JB Chemicals and Pharmaceuticals Limited",
            "JKCEMENT.NS": "JK Cement Limited", "JKLAKSHMI.NS": "JK Lakshmi Cement Limited", "JMFINANCIL.NS": "JM Financial Limited",
            "JSWENERGY.NS": "JSW Energy Limited", "JUSTDIAL.NS": "Just Dial Limited", "KANSAINER.NS": "Kansai Nerolac Paints Limited",
            "KEI.NS": "KEI Industries Limited", "KPITTECH.NS": "KPIT Technologies Limited", "KRBL.NS": "KRBL Limited",
            "LALPATHLAB.NS": "Dr. Lal PathLabs Limited", "LATENTVIEW.NS": "Latent View Analytics Limited", "LAURUSLABS.NS": "Laurus Labs Limited",
            "LEMONTREE.NS": "Lemon Tree Hotels Limited", "LINDEINDIA.NS": "Linde India Limited", "LXCHEM.NS": "Laxmi Organic Industries Limited",
            "MANAPPURAM.NS": "Manappuram Finance Limited", "MAXHEALTH.NS": "Max Healthcare Institute Limited", "MFSL.NS": "Max Financial Services Limited",
            "MIDHANI.NS": "Mishra Dhatu Nigam Limited", "MMTC.NS": "MMTC Limited", "MOIL.NS": "MOIL Limited",
            "MOTILALOFS.NS": "Motilal Oswal Financial Services Limited", "NATCOPHARM.NS": "Natco Pharma Limited", "NAUKRI.NS": "Info Edge (India) Limited",
            "NAVINFLUOR.NS": "Navin Fluorine International Limited", "NFL.NS": "National Fertilizers Limited", "NIITLTD.NS": "NIIT Limited",
            "NOCIL.NS": "NOCIL Limited", "ORIENTELEC.NS": "Orient Electric Limited", "PERSISTENT.NS": "Persistent Systems Limited",
            "PFC.NS": "Power Finance Corporation Limited", "PIRAMALENT.NS": "Piramal Enterprises Limited", "POLICYBZR.NS": "PB Fintech Limited",
            "POLYMED.NS": "Poly Medicure Limited", "PRSMJOHNSN.NS": "Prism Johnson Limited", "RADICO.NS": "Radico Khaitan Limited",
            "RAJESHEXPO.NS": "Rajesh Exports Limited", "RALLIS.NS": "Rallis India Limited", "RAMCOCEM.NS": "The Ramco Cements Limited",
            "RATNAMANI.NS": "Ratnamani Metals & Tubes Limited", "RELAXO.NS": "Relaxo Footwears Limited", "RITES.NS": "RITES Limited",
            "ROUTE.NS": "Route Mobile Limited", "RUPA.NS": "Rupa & Company Limited", "SCHAEFFLER.NS": "Schaeffler India Limited",
            "SEQUENT.NS": "Sequent Scientific Limited", "SFL.NS": "Sheela Foam Limited", "SHANKARA.NS": "Shankara Building Products Limited",
            "SHOPERSTOP.NS": "Shoppers Stop Limited", "SOBHA.NS": "Sobha Limited", "SOLARA.NS": "Solara Active Pharma Sciences Limited",
            "SONACOMS.NS": "Sona BLW Precision Forgings Limited", "SPANDANA.NS": "Spandana Sphoorty Financial Limited", "STARHEALTH.NS": "Star Health and Allied Insurance Company Limited",
            "SUMICHEM.NS": "Sumitomo Chemical India Limited", "SUVEN.NS": "Suven Pharmaceuticals Limited", "SYMPHONY.NS": "Symphony Limited",
            "TTKPRESTIG.NS": "TTK Prestige Limited", "UJJIVAN.NS": "Ujjivan Financial Services Limited", "VAKRANGEE.NS": "Vakrangee Limited",
            "VINATIORGA.NS": "Vinati Organics Limited", "VTL.NS": "Vardhman Textiles Limited", "WELCORP.NS": "Welspun Corp Limited",
            "WOCKPHARMA.NS": "Wockhardt Limited", "ZENSARTECH.NS": "Zensar Technologies Limited", "ZOMATO.NS": "Zomato Limited"
        },
        
        'bse_major': {
            # BSE Major Stocks with BSE Codes
            "500325.BO": "Reliance Industries Limited", "500820.BO": "Asian Paints Limited", "500510.BO": "Larsen & Toubro Limited",
            "532500.BO": "Maruti Suzuki India Limited", "524715.BO": "Sun Pharmaceutical Industries Limited", "507685.BO": "Wipro Limited",
            "532538.BO": "UltraTech Cement Limited", "500770.BO": "Titan Company Limited", "500114.BO": "HCL Technologies Limited",
            "500312.BO": "Oil and Natural Gas Corporation Limited", "500034.BO": "Bajaj Finance Limited", "500090.BO": "Mahindra & Mahindra Limited",
            "532555.BO": "NTPC Limited", "500400.BO": "Power Grid Corporation of India Limited", "500800.BO": "JSW Steel Limited",
            "500570.BO": "Tata Steel Limited", "532755.BO": "Tech Mahindra Limited", "500790.BO": "Nestle India Limited",
            "509480.BO": "Berger Paints India Limited", "500440.BO": "Hindalco Industries Limited", "532281.BO": "Dabur India Limited",
            "532394.BO": "Godrej Consumer Products Limited", "500645.BO": "Trent Limited", "532488.BO": "Dixon Technologies (India) Limited",
            "500471.BO": "TVS Motor Company Limited", "500482.BO": "Britannia Industries Limited", "500495.BO": "Voltas Limited",
            "532424.BO": "Godrej Properties Limited", "500630.BO": "Gillette India Limited", "500182.BO": "Hero MotoCorp Limited",
            "540777.BO": "Polycab India Limited", "532930.BO": "KEI Industries Limited", "540005.BO": "Laurus Labs Limited",
            "532729.BO": "Alkem Laboratories Limited", "532515.BO": "Whirlpool of India Limited", "539523.BO": "Amber Enterprises India Limited",
            "532899.BO": "CRISIL Limited", "532216.BO": "TV18 Broadcast Limited", "500002.BO": "ABB India Limited",
            "500003.BO": "Aegis Logistics Limited", "500008.BO": "Amaraja Batteries Limited", "500010.BO": "Bharat Heavy Electricals Limited",
            "500012.BO": "Bank of Baroda", "500013.BO": "Bank of India", "500020.BO": "Bombay Dyeing & Manufacturing Company Limited",
            "500023.BO": "BEML Limited", "500031.BO": "Bajaj Holdings & Investment Limited", "500032.BO": "BSE Limited",
            "500033.BO": "Bajaj Auto Limited", "500036.BO": "Balrampur Chini Mills Limited", "500038.BO": "Bharat Forge Limited",
            "500043.BO": "Britannia Industries Limited", "500044.BO": "Castrol India Limited", "500049.BO": "Chemplast Sanmar Limited",
            "500051.BO": "Cipla Limited", "500052.BO": "Container Corporation of India Limited", "500054.BO": "Coromandel International Limited",
            "500056.BO": "CRISIL Limited", "500059.BO": "Crompton Greaves Consumer Electricals Limited", "500060.BO": "Cummins India Limited"
        },
        
        'sector_wise': {
            'Banking_Finance': {
                "HDFCBANK.NS": "HDFC Bank Limited", "ICICIBANK.NS": "ICICI Bank Limited", "SBIN.NS": "State Bank of India",
                "KOTAKBANK.NS": "Kotak Mahindra Bank Limited", "AXISBANK.NS": "Axis Bank Limited", "INDUSINDBK.NS": "IndusInd Bank Limited",
                "BAJFINANCE.NS": "Bajaj Finance Limited", "BAJAJFINSV.NS": "Bajaj Finserv Limited", "PNB.NS": "Punjab National Bank",
                "CANBK.NS": "Canara Bank", "BANKBARODA.NS": "Bank of Baroda", "BANKINDIA.NS": "Bank of India",
                "FEDERALBNK.NS": "The Federal Bank Limited", "RBLBANK.NS": "RBL Bank Limited", "IDFCFIRSTB.NS": "IDFC First Bank Limited",
                "YESBANK.NS": "Yes Bank Limited", "AUBANK.NS": "AU Small Finance Bank Limited", "BANDHANBNK.NS": "Bandhan Bank Limited",
                "CHOLAFIN.NS": "Cholamandalam Investment and Finance Company Limited", "MANAPPURAM.NS": "Manappuram Finance Limited",
                "MUTHOOTFIN.NS": "Muthoot Finance Limited", "LICHSGFIN.NS": "LIC Housing Finance Limited", "CANFINHOME.NS": "Can Fin Homes Limited",
                "HDFCLIFE.NS": "HDFC Life Insurance Company Limited", "SBILIFE.NS": "SBI Life Insurance Company Limited",
                "ICICIPRULI.NS": "ICICI Prudential Life Insurance Company Limited", "MAXHEALTH.NS": "Max Healthcare Institute Limited"
            },
            'Information_Technology': {
                "TCS.NS": "Tata Consultancy Services Limited", "INFY.NS": "Infosys Limited", "WIPRO.NS": "Wipro Limited",
                "HCLTECH.NS": "HCL Technologies Limited", "TECHM.NS": "Tech Mahindra Limited", "MINDTREE.NS": "Mindtree Limited",
                "MPHASIS.NS": "Mphasis Limited", "COFORGE.NS": "Coforge Limited", "PERSISTENT.NS": "Persistent Systems Limited",
                "FSL.NS": "Firstsource Solutions Limited", "KPITTECH.NS": "KPIT Technologies Limited", "ZENSAR.NS": "Zensar Technologies Limited",
                "OFSS.NS": "Oracle Financial Services Software Limited", "INTELLECT.NS": "Intellect Design Arena Limited",
                "NIITLTD.NS": "NIIT Limited", "ROUTE.NS": "Route Mobile Limited", "LATENTVIEW.NS": "Latent View Analytics Limited"
            },
            'FMCG_Consumer': {
                "HINDUNILVR.NS": "Hindustan Unilever Limited", "ITC.NS": "ITC Limited", "NESTLEIND.NS": "Nestle India Limited",
                "TITAN.NS": "Titan Company Limited", "BRITANNIA.NS": "Britannia Industries Limited", "DABUR.NS": "Dabur India Limited",
                "GODREJCP.NS": "Godrej Consumer Products Limited", "MARICO.NS": "Marico Limited", "COLPAL.NS": "Colgate Palmolive (India) Limited",
                "PGHH.NS": "Procter & Gamble Hygiene and Health Care Limited", "EMAMILTD.NS": "Emami Limited", "VGUARD.NS": "V-Guard Industries Limited",
                "RELAXO.NS": "Relaxo Footwears Limited", "BATAINDIA.NS": "Bata India Limited", "PAGEIND.NS": "Page Industries Limited",
                "TRENT.NS": "Trent Limited", "SHOPERSTOP.NS": "Shoppers Stop Limited", "JUBLFOOD.NS": "Jubilant FoodWorks Limited",
                "TATACONSUM.NS": "Tata Consumer Products Limited", "UBL.NS": "United Breweries Limited", "RADICO.NS": "Radico Khaitan Limited"
            },
            'Energy_Oil_Gas': {
                "RELIANCE.NS": "Reliance Industries Limited", "ONGC.NS": "Oil and Natural Gas Corporation Limited",
                "BPCL.NS": "Bharat Petroleum Corporation Limited", "IOC.NS": "Indian Oil Corporation Limited",
                "HINDPETRO.NS": "Hindustan Petroleum Corporation Limited", "COALINDIA.NS": "Coal India Limited",
                "NTPC.NS": "NTPC Limited", "POWERGRID.NS": "Power Grid Corporation of India Limited",
                "GAIL.NS": "GAIL (India) Limited", "PETRONET.NS": "Petronet LNG Limited", "IGL.NS": "Indraprastha Gas Limited",
                "GUJGASLTD.NS": "Gujarat Gas Limited", "ADANIPOWER.NS": "Adani Power Limited", "ADANIGREEN.NS": "Adani Green Energy Limited",
                "TATAPOWER.NS": "Tata Power Company Limited", "TORNTPOWER.NS": "Torrent Power Limited", "JSWENERGY.NS": "JSW Energy Limited",
                "PFC.NS": "Power Finance Corporation Limited", "RECLTD.NS": "REC Limited"
            },
            'Automotive': {
                "MARUTI.NS": "Maruti Suzuki India Limited", "TATAMOTORS.NS": "Tata Motors Limited", "M&M.NS": "Mahindra & Mahindra Limited",
                "BAJAJ-AUTO.NS": "Bajaj Auto Limited", "EICHERMOT.NS": "Eicher Motors Limited", "HEROMOTOCO.NS": "Hero MotoCorp Limited",
                "ASHOKLEY.NS": "Ashok Leyland Limited", "ESCORTS.NS": "Escorts Limited", "APOLLOTYRE.NS": "Apollo Tyres Limited",
                "MRF.NS": "MRF Limited", "BALKRISIND.NS": "Balkrishna Industries Limited", "MOTHERSON.NS": "Motherson Sumi Systems Limited",
                "BHARATFORG.NS": "Bharat Forge Limited", "BOSCHLTD.NS": "Bosch Limited", "EXIDEIND.NS": "Exide Industries Limited",
                "SONACOMS.NS": "Sona BLW Precision Forgings Limited"
            },
            'Pharmaceuticals': {
                "SUNPHARMA.NS": "Sun Pharmaceutical Industries Limited", "DRREDDY.NS": "Dr. Reddy's Laboratories Limited",
                "CIPLA.NS": "Cipla Limited", "DIVISLAB.NS": "Divi's Laboratories Limited", "LUPIN.NS": "Lupin Limited",
                "BIOCON.NS": "Biocon Limited", "CADILAHC.NS": "Cadila Healthcare Limited", "AUROPHARMA.NS": "Aurobindo Pharma Limited",
                "TORNTPHARM.NS": "Torrent Pharmaceuticals Limited", "GLENMARK.NS": "Glenmark Pharmaceuticals Limited",
                "ALKEM.NS": "Alkem Laboratories Limited", "IPCALAB.NS": "IPCA Laboratories Limited", "LALPATHLAB.NS": "Dr. Lal PathLabs Limited",
                "LAURUSLABS.NS": "Laurus Labs Limited", "GRANULES.NS": "Granules India Limited", "JBCHEPHARM.NS": "JB Chemicals and Pharmaceuticals Limited",
                "NATCOPHARM.NS": "Natco Pharma Limited", "SOLARA.NS": "Solara Active Pharma Sciences Limited", "WOCKPHARMA.NS": "Wockhardt Limited",
                "PFIZER.NS": "Pfizer Limited", "SUVEN.NS": "Suven Pharmaceuticals Limited"
            },
            'Metals_Mining': {
                "TATASTEEL.NS": "Tata Steel Limited", "JSWSTEEL.NS": "JSW Steel Limited", "HINDALCO.NS": "Hindalco Industries Limited",
                "VEDL.NS": "Vedanta Limited", "NMDC.NS": "NMDC Limited", "JINDALSTEL.NS": "Jindal Steel & Power Limited",
                "SAIL.NS": "Steel Authority of India Limited", "MOIL.NS": "MOIL Limited", "RATNAMANI.NS": "Ratnamani Metals & Tubes Limited",
                "WELCORP.NS": "Welspun Corp Limited", "GRAPHITE.NS": "Graphite India Limited"
            },
            'Infrastructure_Construction': {
                "LT.NS": "Larsen & Toubro Limited", "ULTRACEMCO.NS": "UltraTech Cement Limited", "GRASIM.NS": "Grasim Industries Limited",
                "SHREECEM.NS": "Shree Cement Limited", "ACC.NS": "ACC Limited", "AMBUJACEM.NS": "Ambuja Cements Limited",
                "RAMCOCEM.NS": "The Ramco Cements Limited", "JKCEMENT.NS": "JK Cement Limited", "JKLAKSHMI.NS": "JK Lakshmi Cement Limited",
                "IRB.NS": "IRB Infrastructure Developers Limited", "GMRINFRA.NS": "GMR Infrastructure Limited", "SOBHA.NS": "Sobha Limited",
                "DLF.NS": "DLF Limited", "GODREJPROP.NS": "Godrej Properties Limited", "OBEROIRLTY.NS": "Oberoi Realty Limited",
                "PHOENIXMILLS.NS": "The Phoenix Mills Limited", "CONCOR.NS": "Container Corporation of India Limited"
            }
        }
    }

@st.cache_data(ttl=180, show_spinner=False)
def fetch_stock_data(symbol, period="6mo"):
    """Enhanced stock data fetching with fallbacks"""
    try:
        for p in [period, "3mo", "1y", "2y"]:
            data = yf.download(symbol, period=p, progress=False, auto_adjust=True, timeout=10)
            if not data.empty and len(data) >= 20:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = [col[0] for col in data.columns]
                return data.dropna()
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def intelligent_symbol_search(user_input):
    """Advanced symbol search with fuzzy matching"""
    user_input = user_input.upper().strip()
    variations = [user_input]
    
    # Add exchange suffixes if missing
    if '.' not in user_input:
        variations.extend([f"{user_input}.NS", f"{user_input}.BO"])
    
    # Cross-exchange variations
    if '.NS' in user_input:
        variations.append(user_input.replace('.NS', '.BO'))
    elif '.BO' in user_input:
        variations.append(user_input.replace('.BO', '.NS'))
    
    # Common symbol corrections
    symbol_corrections = {
        'HEROMOTOCO': ['HEROMOTOCO.NS', 'BAJAJ-AUTO.NS', 'EICHERMOT.NS'],
        'HERO': ['HEROMOTOCO.NS', 'BAJAJ-AUTO.NS'],
        'BAJAJ': ['BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS'],
        'HDFC': ['HDFCBANK.NS', 'HDFCLIFE.NS', 'HDFCAMC.NS'],
        'TATA': ['TCS.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TATAPOWER.NS'],
        'ADANI': ['ADANIENT.NS', 'ADANIPORTS.NS', 'ADANIGREEN.NS', 'ADANIPOWER.NS']
    }
    
    base_symbol = user_input.replace('.NS', '').replace('.BO', '')
    if base_symbol in symbol_corrections:
        variations.extend(symbol_corrections[base_symbol])
    
    # Fuzzy matching for company names
    all_stocks = get_all_indian_stocks()
    for category in all_stocks.values():
        for symbol, name in category.items():
            if user_input.lower() in name.lower() or user_input.lower() in symbol.lower():
                variations.append(symbol)
    
    return list(dict.fromkeys(variations))[:10]  # Limit to top 10 variations

def calculate_advanced_technical_score(df):
    """Professional 20-point technical scoring system"""
    if df.empty or len(df) < 20:
        return None, 0, []
    
    try:
        close = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        volume = df['Volume'].values
        
        score = 0
        signals = []
        
        # Calculate technical indicators
        rsi = calculate_rsi(close, 14)
        macd_line, macd_signal = calculate_macd(close)
        sma20 = pd.Series(close).rolling(20, min_periods=1).mean().values
        sma50 = pd.Series(close).rolling(50, min_periods=1).mean().values
        ema20 = pd.Series(close).ewm(span=20, min_periods=1).mean().values
        
        # 1. RSI Analysis (0-3 points)
        current_rsi = rsi[-1]
        if 55 <= current_rsi <= 75:
            score += 3; signals.append("🚀 RSI Strong Momentum Zone")
        elif 45 <= current_rsi <= 55:
            score += 2; signals.append("📈 RSI Neutral Bullish")
        elif current_rsi < 30:
            score += 2; signals.append("💎 RSI Oversold Opportunity")
        elif current_rsi > 80:
            score -= 1; signals.append("⚠️ RSI Extreme Overbought")
        
        # 2. MACD Analysis (0-3 points)
        if len(macd_line) > 1:
            if macd_line[-1] > macd_signal[-1] and macd_line[-2] <= macd_signal[-2]:
                score += 3; signals.append("🎯 MACD Fresh Bullish Crossover")
            elif macd_line[-1] > macd_signal[-1]:
                score += 2; signals.append("⚡ MACD Bullish Trend")
            elif macd_line[-1] > 0:
                score += 1; signals.append("📊 MACD Above Zero Line")
        
        # 3. Volume Analysis (0-4 points)
        recent_volume = np.mean(volume[-3:])
        avg_volume = np.mean(volume[-20:])
        volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
        
        if volume_ratio >= 3.0:
            score += 4; signals.append("🔥 Explosive Volume Surge")
        elif volume_ratio >= 2.0:
            score += 3; signals.append("📊 High Volume Breakout")
        elif volume_ratio >= 1.5:
            score += 2; signals.append("📈 Above Average Volume")
        elif volume_ratio >= 1.2:
            score += 1; signals.append("💹 Moderate Volume Increase")
        
        # 4. Price Momentum Analysis (0-4 points)
        price_1d = (close[-1] - close[-2]) / close[-2] if len(close) >= 2 else 0
        price_5d = (close[-1] - close[-6]) / close[-6] if len(close) >= 6 else 0
        price_10d = (close[-1] - close[-11]) / close[-11] if len(close) >= 11 else 0
        
        if price_1d > 0.05:  # 5%+ daily gain
            score += 2; signals.append("🚁 Strong Daily Momentum +5%")
        elif price_1d > 0.02:  # 2%+ daily gain
            score += 1; signals.append("📈 Good Daily Move +2%")
        
        if price_5d > 0.10:  # 10%+ weekly gain
            score += 2; signals.append("💎 Excellent Weekly Performance +10%")
        elif price_5d > 0.05:  # 5%+ weekly gain
            score += 1; signals.append("✅ Strong Weekly Trend +5%")
        
        # 5. Breakout Analysis (0-3 points)
        high_20 = np.max(high[-20:]) if len(high) >= 20 else high[-1]
        high_52w = np.max(high[-252:]) if len(high) >= 252 else high_20
        
        if close[-1] >= high_52w:
            score += 3; signals.append("🎯 52-Week High Breakout")
        elif close[-1] >= high_20:
            score += 2; signals.append("🚀 20-Day High Breakout")
        elif close[-1] >= high_20 * 0.98:
            score += 1; signals.append("⚠️ Near 20-Day High")
        
        # 6. Moving Average Analysis (0-3 points)
        if close[-1] > ema20[-1] > sma20[-1] > sma50[-1]:
            score += 3; signals.append("🔥 Perfect Moving Average Stack")
        elif close[-1] > sma20[-1] > sma50[-1]:
            score += 2; signals.append("📈 Bullish MA Alignment")
        elif close[-1] > sma20[-1]:
            score += 1; signals.append("✅ Above Short-term MA")
        
        # Add all indicators to dataframe
        df_result = df.copy()
        df_result['RSI'] = pd.Series(rsi, index=df.index)
        df_result['MACD'] = pd.Series(macd_line, index=df.index)
        df_result['MACD_Signal'] = pd.Series(macd_signal, index=df.index)
        df_result['SMA20'] = pd.Series(sma20, index=df.index)
        df_result['SMA50'] = pd.Series(sma50, index=df.index)
        df_result['EMA20'] = pd.Series(ema20, index=df.index)
        df_result['Volume_Ratio'] = volume_ratio
        df_result['Price_1D'] = price_1d * 100
        df_result['Price_5D'] = price_5d * 100
        df_result['Price_10D'] = price_10d * 100
        
        return df_result, min(score, 20), signals
    
    except Exception as e:
        return df, 0, []

def calculate_rsi(prices, period=14):
    """RSI Calculation"""
    delta = np.diff(prices, prepend=prices[0])
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(period, min_periods=1).mean().values
    avg_loss = pd.Series(loss).rolling(period, min_periods=1).mean().values
    avg_loss = np.where(avg_loss == 0, 1e-10, avg_loss)
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """MACD Calculation"""
    ema_fast = pd.Series(prices).ewm(span=fast, min_periods=1).mean().values
    ema_slow = pd.Series(prices).ewm(span=slow, min_periods=1).mean().values
    macd_line = ema_fast - ema_slow
    macd_signal = pd.Series(macd_line).ewm(span=signal, min_periods=1).mean().values
    return macd_line, macd_signal

def parallel_stock_analysis(stocks_dict, min_score=8, max_results=150):
    """High-performance parallel stock analysis"""
    def analyze_single_stock(item):
        symbol, name = item
        try:
            df = fetch_stock_data(symbol)
            if not df.empty:
                processed_df, score, signals = calculate_advanced_technical_score(df)
                if processed_df is not None and score >= min_score:
                    current = processed_df['Close'].iloc[-1]
                    prev = processed_df['Close'].iloc[-2] if len(processed_df) > 1 else current
                    change_1d = ((current - prev) / prev) * 100 if prev > 0 else 0
                    change_5d = processed_df['Price_5D'].iloc[-1] if 'Price_5D' in processed_df.columns else 0
                    rsi_val = processed_df['RSI'].iloc[-1] if 'RSI' in processed_df.columns else 50
                    vol_ratio = processed_df['Volume_Ratio'].iloc[-1] if 'Volume_Ratio' in processed_df.columns else 1
                    
                    return {
                        'Symbol': symbol.replace('.NS', '').replace('.BO', ''),
                        'Company': name[:30] + "..." if len(name) > 30 else name,
                        'Price': f"₹{current:.2f}",
                        '1D%': f"{change_1d:+.1f}%",
                        '5D%': f"{change_5d:+.1f}%",
                        'RSI': f"{rsi_val:.0f}",
                        'Volume': f"{vol_ratio:.1f}x",
                        'Score': f"{score}/20",
                        'TopSignal': signals[0] if signals else "Mixed Signals",
                        'AllSignals': signals,
                        'Data': processed_df,
                        'NumScore': score,
                        'NumChange1D': change_1d,
                        'NumChange5D': change_5d,
                        'NumRSI': rsi_val,
                        'NumVolRatio': vol_ratio,
                        'OriginalSymbol': symbol
                    }
        except Exception as e:
            pass
        return None
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(analyze_single_stock, item) for item in stocks_dict.items()]
        for future in concurrent.futures.as_completed(futures, timeout=120):
            try:
                result = future.result(timeout=15)
                if result:
                    results.append(result)
            except Exception:
                continue
    
    return sorted(results, key=lambda x: x['NumScore'], reverse=True)[:max_results]

def create_tradingview_chart(df, symbol):
    """Professional TradingView-style charts"""
    colors = {
        'bg': '#131722',
        'up_candle': '#26a69a',
        'down_candle': '#ef5350',
        'up_volume': '#26a69a',
        'down_volume': '#ef5350',
        'sma20': '#2196f3',
        'sma50': '#ff9800',
        'ema20': '#9c27b0',
        'rsi': '#00bcd4',
        'macd': '#4caf50',
        'signal': '#f44336',
        'grid': '#363a45',
        'text': '#d1d4dc'
    }
    
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.5, 0.15, 0.2, 0.15],
        subplot_titles=(
            f"🚀 {symbol} - Professional Analysis",
            "📊 RSI (14)",
            "⚡ MACD (12,26,9)",
            "📈 Volume Analysis"
        )
    )
    
    # Main Candlestick Chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='OHLC',
        increasing_line_color=colors['up_candle'],
        decreasing_line_color=colors['down_candle'],
        increasing_fillcolor=colors['up_candle'],
        decreasing_fillcolor=colors['down_candle']
    ), row=1, col=1)
    
    # Moving Averages
    if 'SMA20' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA20'],
            name='SMA 20',
            line=dict(color=colors['sma20'], width=2)
        ), row=1, col=1)
    
    if 'SMA50' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['SMA50'],
            name='SMA 50',
            line=dict(color=colors['sma50'], width=2)
        ), row=1, col=1)
    
    if 'EMA20' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['EMA20'],
            name='EMA 20',
            line=dict(color=colors['ema20'], width=2, dash='dash')
        ), row=1, col=1)
    
    # RSI
    if 'RSI' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['RSI'],
            name='RSI',
            line=dict(color=colors['rsi'], width=2)
        ), row=2, col=1)
        
        # RSI levels
        fig.add_hline(y=70, line=dict(color=colors['down_candle'], dash='dash'), row=2, col=1)
        fig.add_hline(y=30, line=dict(color=colors['up_candle'], dash='dash'), row=2, col=1)
        fig.add_hline(y=50, line=dict(color=colors['text'], dash='dot', width=1), row=2, col=1)
    
    # MACD
    if 'MACD' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['MACD'],
            name='MACD',
            line=dict(color=colors['macd'], width=2)
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index, y=df['MACD_Signal'],
            name='Signal',
            line=dict(color=colors['signal'], width=2)
        ), row=3, col=1)
        
        # MACD Histogram
        if len(df) > 0:
            macd_hist = df['MACD'] - df['MACD_Signal']
            hist_colors = [colors['up_candle'] if x >= 0 else colors['down_candle'] for x in macd_hist]
            fig.add_trace(go.Bar(
                x=df.index, y=macd_hist,
                name='MACD Histogram',
                marker_color=hist_colors,
                opacity=0.7
            ), row=3, col=1)
        
        fig.add_hline(y=0, line=dict(color=colors['text'], dash='solid'), row=3, col=1)
    
    # Volume
    volume_colors = [colors['up_volume'] if df['Close'].iloc[i] >= df['Open'].iloc[i] 
                    else colors['down_volume'] for i in range(len(df))]
    
    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'],
        name='Volume',
        marker_color=volume_colors,
        opacity=0.7
    ), row=4, col=1)
    
    # Layout styling
    fig.update_layout(
        height=900,
        paper_bgcolor=colors['bg'],
        plot_bgcolor=colors['bg'],
        font=dict(color=colors['text'], family='Trebuchet MS'),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor=colors['bg'],
            bordercolor=colors['grid'],
            borderwidth=1
        ),
        title=dict(
            text=f"Professional Technical Analysis - {symbol}",
            font=dict(size=16, color=colors['text']),
            x=0.5
        ),
        xaxis_rangeslider_visible=False
    )
    
    # Update axes
    for i in range(1, 5):
        fig.update_xaxes(
            gridcolor=colors['grid'],
            showgrid=True,
            zeroline=False,
            row=i, col=1
        )
        fig.update_yaxes(
            gridcolor=colors['grid'],
            showgrid=True,
            zeroline=False,
            row=i, col=1
        )
    
    return fig

# MARKET STATUS
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST)
is_market_open = (
    current_time.weekday() < 5 and 
    current_time.replace(hour=9, minute=15) <= current_time <= current_time.replace(hour=15, minute=30)
)

# MAIN APPLICATION
def main():
    # Header
    st.markdown('<h1 id="header">📊 TradingView Pro - Indian Stock Screener</h1>', unsafe_allow_html=True)
    
    # Market Status
    market_status = "🟢 LIVE TRADING" if is_market_open else "🔴 MARKET CLOSED"
    st.markdown(f'''
    <div class="tv-market-status">
        {market_status} | {current_time.strftime('%A, %d %B %Y')} | {current_time.strftime('%I:%M %p IST')}
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar Controls
    with st.sidebar:
        st.markdown("### ⚙️ Professional Controls")
        
        min_score = st.slider("Technical Score Filter:", 5, 20, 10, 
                             help="Minimum technical score (higher = more selective)")
        max_results = st.slider("Results Limit:", 25, 200, 100, 
                               help="Maximum number of stocks to display")
        
        st.markdown("### 📊 Market Coverage")
        coverage_option = st.selectbox(
            "Select Market Coverage:",
            [
                "Popular Stocks (~100)",
                "Large Cap NSE (~150)",
                "Large + Mid Cap NSE (~300)", 
                "Complete NSE (~500)",
                "NSE + BSE Complete (~700)"
            ],
            index=2
        )
        
        st.markdown("### 🔍 Advanced Filters")
        volume_filter = st.selectbox(
            "Volume Filter:",
            ["All Volumes", "Above Average (>1.2x)", "High Volume (>1.5x)", 
             "Very High (>2x)", "Explosive (>3x)"]
        )
        
        rsi_filter = st.selectbox(
            "RSI Filter:",
            ["All RSI Levels", "Oversold (<30)", "Buy Zone (30-50)", 
             "Momentum Zone (50-75)", "Overbought (>75)"]
        )
        
        price_filter = st.selectbox(
            "Price Movement:",
            ["All Movements", "Gainers Only", "Strong Gainers (+2%)", 
             "Big Movers (+5%)", "Weekly Winners (+10%)"]
        )
        
        if st.button("🔄 Refresh All Data"):
            st.cache_data.clear()
            st.rerun()
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚀 Pro Screener", 
        "🏭 Sector Analysis", 
        "🔍 Stock Research",
        "📈 Watchlist Pro",
        "📊 Market Dashboard"
    ])
    
    with tab1:
        st.markdown("### 🚀 Professional Stock Screener")
        st.markdown(f"**Real-time screening across Indian stock markets with advanced technical analysis**")
        
        if st.button("🚀 **LAUNCH PRO SCREENER**", type="primary"):
            # Get stock universe based on coverage option
            all_stocks = get_all_indian_stocks()
            
            if coverage_option == "Popular Stocks (~100)":
                stocks_to_scan = dict(list(all_stocks['nse_large_cap'].items())[:50])
                stocks_to_scan.update(dict(list(all_stocks['nse_mid_cap'].items())[:50]))
            elif coverage_option == "Large Cap NSE (~150)":
                stocks_to_scan = all_stocks['nse_large_cap']
                stocks_to_scan.update(dict(list(all_stocks['nse_mid_cap'].items())[:50]))
            elif coverage_option == "Large + Mid Cap NSE (~300)":
                stocks_to_scan = {**all_stocks['nse_large_cap'], **all_stocks['nse_mid_cap']}
            elif coverage_option == "Complete NSE (~500)":
                stocks_to_scan = {**all_stocks['nse_large_cap'], **all_stocks['nse_mid_cap'], **all_stocks['nse_small_cap']}
            else:  # NSE + BSE Complete
                stocks_to_scan = {**all_stocks['nse_large_cap'], **all_stocks['nse_mid_cap'], 
                                **all_stocks['nse_small_cap'], **all_stocks['bse_major']}
            
            st.info(f"🔍 **Screening {len(stocks_to_scan)} stocks** from {coverage_option}")
            
            with st.spinner('⚡ Professional analysis in progress...'):
                results = parallel_stock_analysis(stocks_to_scan, min_score, max_results)
            
            # Apply filters
            if results:
                filtered_results = results.copy()
                
                # Volume filtering
                if volume_filter == "Above Average (>1.2x)":
                    filtered_results = [r for r in filtered_results if r['NumVolRatio'] >= 1.2]
                elif volume_filter == "High Volume (>1.5x)":
                    filtered_results = [r for r in filtered_results if r['NumVolRatio'] >= 1.5]
                elif volume_filter == "Very High (>2x)":
                    filtered_results = [r for r in filtered_results if r['NumVolRatio'] >= 2.0]
                elif volume_filter == "Explosive (>3x)":
                    filtered_results = [r for r in filtered_results if r['NumVolRatio'] >= 3.0]
                
                # RSI filtering
                if rsi_filter == "Oversold (<30)":
                    filtered_results = [r for r in filtered_results if r['NumRSI'] < 30]
                elif rsi_filter == "Buy Zone (30-50)":
                    filtered_results = [r for r in filtered_results if 30 <= r['NumRSI'] <= 50]
                elif rsi_filter == "Momentum Zone (50-75)":
                    filtered_results = [r for r in filtered_results if 50 <= r['NumRSI'] <= 75]
                elif rsi_filter == "Overbought (>75)":
                    filtered_results = [r for r in filtered_results if r['NumRSI'] > 75]
                
                # Price filtering
                if price_filter == "Gainers Only":
                    filtered_results = [r for r in filtered_results if r['NumChange1D'] > 0]
                elif price_filter == "Strong Gainers (+2%)":
                    filtered_results = [r for r in filtered_results if r['NumChange1D'] > 2]
                elif price_filter == "Big Movers (+5%)":
                    filtered_results = [r for r in filtered_results if r['NumChange1D'] > 5]
                elif price_filter == "Weekly Winners (+10%)":
                    filtered_results = [r for r in filtered_results if r['NumChange5D'] > 10]
                
                if filtered_results:
                    st.success(f"🎯 **Professional Screening Complete! {len(filtered_results)} high-quality opportunities identified**")
                    
                    # Professional summary metrics
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    total_found = len(filtered_results)
                    avg_score = sum(r['NumScore'] for r in filtered_results) / len(filtered_results)
                    excellent_picks = len([r for r in filtered_results if r['NumScore'] >= 16])
                    strong_picks = len([r for r in filtered_results if r['NumScore'] >= 12])
                    positive_momentum = len([r for r in filtered_results if r['NumChange1D'] > 0])
                    
                    with col1:
                        st.markdown(f'''
                        <div class="tv-card bullish">
                            <h4>Total Opportunities</h4>
                            <h2>{total_found}</h2>
                            <p>Quality Stocks Found</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with col2:
                        score_class = "bullish" if avg_score >= 14 else "neutral" if avg_score >= 10 else "bearish"
                        st.markdown(f'''
                        <div class="tv-card {score_class}">
                            <h4>Average Score</h4>
                            <h2>{avg_score:.1f}/20</h2>
                            <p>Technical Strength</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f'''
                        <div class="tv-card {'bullish' if excellent_picks > 0 else 'neutral'}">
                            <h4>Excellent Picks</h4>
                            <h2>{excellent_picks}</h2>
                            <p>Score ≥ 16/20</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f'''
                        <div class="tv-card {'bullish' if strong_picks > 5 else 'neutral'}">
                            <h4>Strong Signals</h4>
                            <h2>{strong_picks}</h2>
                            <p>Score ≥ 12/20</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with col5:
                        momentum_class = "bullish" if positive_momentum > total_found/2 else "bearish"
                        st.markdown(f'''
                        <div class="tv-card {momentum_class}">
                            <h4>Positive Today</h4>
                            <h2>{positive_momentum}</h2>
                            <p>Daily Gainers</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Professional results table
                    st.markdown("### 📋 Professional Screening Results")
                    
                    display_df = pd.DataFrame([{
                        'Rank': f"#{i+1}",
                        'Symbol': r['Symbol'],
                        'Company': r['Company'],
                        'Price': r['Price'],
                        '1D%': r['1D%'],
                        '5D%': r['5D%'],
                        'RSI': r['RSI'],
                        'Volume': r['Volume'],
                        'Score': r['Score'],
                        'Top Signal': r['TopSignal']
                    } for i, r in enumerate(filtered_results)])
                    
                    st.dataframe(display_df, use_container_width=True, hide_index=True, height=600)
                    
                    # Export functionality
                    csv_data = display_df.to_csv(index=False)
                    timestamp = current_time.strftime('%Y%m%d_%H%M%S')
                    st.download_button(
                        label="📥 **Export Professional Results**",
                        data=csv_data,
                        file_name=f"tradingview_pro_screening_{timestamp}.csv",
                        mime="text/csv",
                        help="Download complete screening results with all metrics"
                    )
                    
                    # Professional Chart Analysis
                    st.markdown("### 📊 Professional Chart Analysis")
                    
                    chart_options = [f"{r['Symbol']} - {r['Company']} (Score: {r['Score']})" for r in filtered_results]
                    selected_for_analysis = st.selectbox(
                        "🎯 Select stock for professional technical analysis:",
                        options=chart_options,
                        help="Choose any stock from screening results for detailed professional analysis"
                    )
                    
                    if selected_for_analysis:
                        selected_symbol = selected_for_analysis.split(' - ')[0]
                        selected_stock = next(r for r in filtered_results if r['Symbol'] == selected_symbol)
                        
                        # Professional metrics dashboard
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        
                        with col1:
                            score_class = "bullish" if selected_stock['NumScore'] >= 16 else "neutral" if selected_stock['NumScore'] >= 12 else "bearish"
                            grade = "A+" if selected_stock['NumScore'] >= 18 else "A" if selected_stock['NumScore'] >= 16 else "B+" if selected_stock['NumScore'] >= 12 else "B" if selected_stock['NumScore'] >= 8 else "C"
                            st.markdown(f'''
                            <div class="tv-card {score_class}">
                                <h4>Technical Grade</h4>
                                <h2>{grade}</h2>
                                <p>{selected_stock['Score']}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col2:
                            change_class = "bullish" if selected_stock['NumChange1D'] > 2 else "neutral" if selected_stock['NumChange1D'] > 0 else "bearish"
                            st.markdown(f'''
                            <div class="tv-card {change_class}">
                                <h4>Current Price</h4>
                                <h2>{selected_stock['Price']}</h2>
                                <p>{selected_stock['1D%']} today</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col3:
                            weekly_class = "bullish" if selected_stock['NumChange5D'] > 5 else "neutral" if selected_stock['NumChange5D'] > 0 else "bearish"
                            st.markdown(f'''
                            <div class="tv-card {weekly_class}">
                                <h4>5-Day Move</h4>
                                <h2>{selected_stock['5D%']}</h2>
                                <p>Weekly Performance</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col4:
                            rsi_class = "bearish" if selected_stock['NumRSI'] > 75 else "bullish" if selected_stock['NumRSI'] < 30 else "neutral"
                            rsi_status = "Overbought" if selected_stock['NumRSI'] > 75 else "Oversold" if selected_stock['NumRSI'] < 30 else "Normal"
                            st.markdown(f'''
                            <div class="tv-card {rsi_class}">
                                <h4>RSI Momentum</h4>
                                <h2>{selected_stock['RSI']}</h2>
                                <p>{rsi_status}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col5:
                            vol_class = "bullish" if selected_stock['NumVolRatio'] >= 2 else "neutral"
                            vol_status = "Explosive" if selected_stock['NumVolRatio'] >= 3 else "High" if selected_stock['NumVolRatio'] >= 2 else "Normal"
                            st.markdown(f'''
                            <div class="tv-card {vol_class}">
                                <h4>Volume Status</h4>
                                <h2>{selected_stock['Volume']}</h2>
                                <p>{vol_status}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col6:
                            rank = next(i+1 for i, r in enumerate(filtered_results) if r['Symbol'] == selected_symbol)
                            rank_class = "bullish" if rank <= 5 else "neutral" if rank <= 20 else "bearish"
                            st.markdown(f'''
                            <div class="tv-card {rank_class}">
                                <h4>Rank</h4>
                                <h2>#{rank}</h2>
                                <p>of {len(filtered_results)}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        # Professional TradingView Chart
                        st.markdown('<div class="tv-chart-container">', unsafe_allow_html=True)
                        fig = create_tradingview_chart(selected_stock['Data'], selected_stock['Symbol'])
                        st.plotly_chart(fig, use_container_width=True, config={
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                            'toImageButtonOptions': {
                                'format': 'png',
                                'filename': f'{selected_stock["Symbol"]}_professional_analysis',
                                'height': 900,
                                'width': 1600,
                                'scale': 2
                            }
                        })
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Professional Analysis Summary
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 🎯 Professional Signals")
                            signals = selected_stock['AllSignals']
                            if signals:
                                for signal in signals[:6]:
                                    if any(emoji in signal for emoji in ["🚀", "🔥", "🎯", "💎"]):
                                        st.success(f"{signal}")
                                    elif any(emoji in signal for emoji in ["⚠️", "📊"]):
                                        st.warning(f"{signal}")
                                    else:
                                        st.info(f"{signal}")
                            else:
                                st.info("📊 Mixed technical signals - monitor for clearer setup")
                        
                        with col2:
                            st.markdown("#### 📊 Professional Recommendation")
                            
                            score = selected_stock['NumScore']
                            if score >= 18:
                                st.success("🚀 **STRONG BUY** - Exceptional technical setup with multiple bullish confirmations")
                                st.markdown('<div class="tv-alert">🚨 TOP TIER OPPORTUNITY ALERT 🚨</div>', unsafe_allow_html=True)
                            elif score >= 16:
                                st.success("📈 **BUY** - Strong technical setup with good risk-reward")
                            elif score >= 12:
                                st.warning("📊 **ACCUMULATE** - Decent setup, consider on dips")
                            elif score >= 8:
                                st.info("👁️ **WATCH** - Monitor for better entry opportunity")
                            else:
                                st.error("⚠️ **AVOID** - Weak technical setup")
                            
                            st.markdown(f"**📊 Professional Grade:** {grade} ({selected_stock['Score']})")
                            st.markdown(f"**🏆 Screening Rank:** #{rank} out of {len(filtered_results)}")
                            st.markdown(f"**📈 Market Coverage:** {coverage_option}")
                
                else:
                    st.info("🔍 No stocks found matching current filter criteria. Try adjusting the filters.")
            else:
                st.info("📊 No opportunities found with current screening parameters. Try lowering the minimum score.")
    
    with tab2:
        st.markdown("### 🏭 Professional Sector Analysis")
        st.markdown("**Comprehensive sector rotation analysis across all major Indian industry segments**")
        
        all_sectors = get_all_indian_stocks()['sector_wise']
        selected_sectors = st.multiselect(
            "🎯 Select sectors for comprehensive analysis:",
            options=list(all_sectors.keys()),
            default=list(all_sectors.keys())[:4],
            help="Choose industry sectors for detailed technical analysis"
        )
        
        if st.button("🏭 **LAUNCH SECTOR ANALYSIS**", type="primary"):
            if selected_sectors:
                all_sector_results = []
                sector_performance = {}
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, sector_name in enumerate(selected_sectors):
                    status_text.text(f'🔍 Analyzing {sector_name.replace("_", " ")} sector...')
                    
                    sector_stocks = all_sectors[sector_name]
                    sector_results = parallel_stock_analysis(sector_stocks, min_score=5, max_results=50)
                    
                    if sector_results:
                        avg_score = sum(r['NumScore'] for r in sector_results) / len(sector_results)
                        avg_change_1d = sum(r['NumChange1D'] for r in sector_results) / len(sector_results)
                        avg_change_5d = sum(r['NumChange5D'] for r in sector_results) / len(sector_results)
                        excellent_count = len([r for r in sector_results if r['NumScore'] >= 16])
                        strong_count = len([r for r in sector_results if r['NumScore'] >= 12])
                        
                        sector_performance[sector_name] = {
                            'results': sector_results,
                            'avg_score': avg_score,
                            'avg_change_1d': avg_change_1d,
                            'avg_change_5d': avg_change_5d,
                            'excellent_count': excellent_count,
                            'strong_count': strong_count,
                            'total_stocks': len(sector_stocks),
                            'qualified_stocks': len(sector_results)
                        }
                        
                        # Add sector info to results
                        for result in sector_results:
                            result['Sector'] = sector_name.replace('_', ' ').title()
                        
                        all_sector_results.extend(sector_results)
                    
                    progress_bar.progress((i + 1) / len(selected_sectors))
                
                progress_bar.empty()
                status_text.empty()
                
                if sector_performance:
                    st.success(f"🎯 **Sector Analysis Complete! Analyzed {len(selected_sectors)} major sectors**")
                    
                    # Sector performance dashboard
                    st.markdown("### 🏆 Sector Performance Rankings")
                    
                    sorted_sectors = sorted(sector_performance.items(), key=lambda x: x[1]['avg_score'], reverse=True)
                    
                    for rank, (sector, data) in enumerate(sorted_sectors, 1):
                        sector_display = sector.replace('_', ' ').title()
                        
                        col1, col2, col3, col4, col5, col6 = st.columns(6)
                        
                        with col1:
                            rank```

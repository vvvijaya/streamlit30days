import streamlit as st
import duckdb, pandas as pd, os 

st.header('Welcome to MIST tool')

#st.write("Die Bank LT in weeks?")
db_lt = st.slider("Die Bank LT in weeks", 1, 52, 1)
st.write(db_lt)
fg_lt = st.slider("FGWH LT in weeks", 1, 26, 1)
st.write(fg_lt)
csl = st.selectbox("CSL:", (90,92.5, 95), help='')/100
st.write(csl)
ss_db = st.toggle("SS in DB?")
st.write(ss_db)
ss_fg = st.toggle("SS in FG?")
st.write(ss_fg)
upside_demand = st.slider("Upside Demand", 0, 50, 5)/100
st.write(upside_demand)
nbr_fg_skus = st.selectbox("Number of FG SKUs per Die Type", (1,2,4,6,8,12), help='Number of FG SKUs per Die Type. If >12, choose 12.')

if st.button("Calculate WOI"):
    df = pd.read_parquet(os.getcwd() + '\\woi_results.parquet')
    df.rename(columns={'Service Level %': 'CSL'}, inplace=True)
    #if Strategic_Inv_Holding_DieBank value is Yes, set it to True
    df['Strategic_Inv_Holding_DieBank'] = df['Strategic_Inv_Holding_DieBank'].apply(lambda x: True if x == 'Yes' else False)
    df['Strategic_Inv_Holding_FGWH'] = df['Strategic_Inv_Holding_FGWH'].apply(lambda x: True if x == 'Yes' else False)
    st.dataframe(duckdb.sql('SELECT total_woi, trdi_woi, fgwh_woi FROM df WHERE WaferStart_To_DieBank_LT_Wks={} and DieBank_To_FG_LT_Wks={} and Nbr_fg_skus_per_DieType={} and Upside_pct_over_LeadTime={} and CSL={} and Strategic_Inv_Holding_DieBank={} and  Strategic_Inv_Holding_FGWH={}'.format(db_lt, fg_lt,nbr_fg_skus, upside_demand,csl, ss_db, ss_fg)).df().head(10))
    #used duckdb.sql() because it took <.1 seconds to run but df.query() took .3 seconds to run (when searching over 22M rows)
    


    




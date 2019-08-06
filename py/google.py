import pygsheets

gc = pygsheets.authorize(service_file='credentials.json')
g_doc = gc.open_by_key('1T67gVealvVutn_VuiedbH7ViK8_OIBWOmoDIMq82oQE')

def get_gsheet(candle_string):
    return g_doc.worksheet_by_title('Crypto - ' + candle_string).get_as_df()

def save_gsheet(candle_string, df):
    return g_doc.worksheet_by_title('Crypto - ' + candle_string).set_dataframe(df, (1,1))

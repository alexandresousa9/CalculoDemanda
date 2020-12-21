import pandas as pd
import datetime

MEDIA_DIARIA = 30

base = pd.read_csv(r'C:\Users\Alexandre\Documents\ItauEstagio\CALCULO_DEMANDA\base_2021.csv')

weekmask = "Mon Tue Wed Thu Fri"

holidays = [datetime.datetime(2021, 12, 31)]


planejamento = pd.bdate_range(start='12/01/2020', 
                        end='12/31/2021',
                        freq='C',
                        weekmask = weekmask,
                        holidays=holidays).to_frame(index=False, name='DIAS_UTEIS').sort_values(by=['DIAS_UTEIS'], ascending=False, ignore_index=True)


#def calcula_saldo(row, data_qtd):
#    data_planejamento = row['DATA_PLANEJAMENTO']
#    return data_qtd[data_planejamento] - MEDIA_DIARIA

#def obtem_qtd_planejados(row):
#    return row['SALDO'] + MEDIA_DIARIA

#data_qtd                    = base['DATA_PLANEJAMENTO'].value_counts()

#base['SALDO']               = base.apply(lambda row: calcula_saldo(row, data_qtd), axis=1)
#base['QTD_PLANEJADA']       = base.apply(lambda row: obtem_qtd_planejados(row), axis=1)



base['DATA_PLANEJAMENTO']   = pd.to_datetime(base['DATA_PLANEJAMENTO'], format="%d/%m/%Y")





db_planejamento      = pd.DataFrame(data=None, columns=base.columns)
db_replanejamento    = pd.DataFrame(data=None, columns=base.columns)


for dia_util in planejamento['DIAS_UTEIS']:

    dataframe_aux1 = None
    dataframe_aux2 = None

    df_planejado = base[base['DATA_PLANEJAMENTO'] == dia_util].reindex()

    if len(df_planejado) >= MEDIA_DIARIA:

        # dados com a data dia_util
        dataframe_aux1 = df_planejado[0:MEDIA_DIARIA]
        dataframe_aux1.loc[:,'DATA_CADASTRO'] = dia_util

        db_planejamento = db_planejamento.append(dataframe_aux1, ignore_index = True)

        # Adicionar na lista de replanejados caso
        # tenha excedido a demanda para o dia.
        if len(df_planejado) > MEDIA_DIARIA:
            dataframe_aux2 = df_planejado[MEDIA_DIARIA:len(df_planejado)]
            db_replanejamento = db_replanejamento.append(dataframe_aux2, ignore_index = True)

    elif len(df_planejado) > 0 or len(db_replanejamento) > 0:
        capacidada_ocupada      = len(df_planejado)
        capacidada_disponivel   = MEDIA_DIARIA - capacidada_ocupada

        # dados com a data dia_util
        dataframe_aux1 = df_planejado[0:capacidada_ocupada]
        dataframe_aux1.loc[:,'DATA_CADASTRO'] = dia_util


        if len(db_replanejamento) > 0:
            if len(db_replanejamento) >= capacidada_disponivel:
                dataframe_aux2 = db_replanejamento[0:capacidada_disponivel]
                db_replanejamento = db_replanejamento[capacidada_disponivel:len(db_replanejamento)]
            else:
                dataframe_aux2 = db_replanejamento[0:len(db_replanejamento)]
                db_replanejamento = pd.DataFrame(data=None, columns=base.columns)

            dataframe_aux2.loc[:,'DATA_CADASTRO'] = dia_util

        db_planejamento = db_planejamento.append(dataframe_aux1, ignore_index = True)
        db_planejamento = db_planejamento.append(dataframe_aux2, ignore_index = True)


print(db_planejamento)
print(db_replanejamento)

db_planejamento.to_csv('base_2021_calculado_demanda_diaria.csv', index=False)

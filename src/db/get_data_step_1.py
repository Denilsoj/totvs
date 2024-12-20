from config import cursor as cur
from config import con







class DB:

    @staticmethod
    def get_data_step_1():
        try:
            sql = 'SELECT * FROM public.dados_tratados WHERE fase = 1 and classificado = true;'
            cur.execute(sql)
            processed_data = cur.fetchall()
            return processed_data
        
        except Exception:
            print('error', Exception)
        finally:
            cur.close()

    @staticmethod
    def get_data_step_1():
        try:
            sql = 'SELECT * FROM public.dados_tratados WHERE fase = 1 and classificado = true;'
            cur.execute(sql)
            processed_data = cur.fetchall()
            return processed_data
        
        except Exception:
            print('error', Exception)
        finally:
            cur.close()
    @staticmethod
    def get_data_step_2():
        try:
            sql = 'SELECT * FROM public.dados_tratados WHERE fase = 1 and classificado = true;'
            cur.execute(sql)
            processed_data = cur.fetchall()
            return processed_data
        
        except Exception:
            print('error', Exception)
        finally:
            cur.close()





            









from src.db.config import ConfigDB

class UpdatedNegativeWords:
    query = """
    UPDATE "{schema_name}"."{table_name}" 
    SET classificacao = true, fase = 1 
    WHERE  conditions"""
    def __init__(self, schema_name, table_name):
        self.schema_name = schema_name
        self.table_name = table_name
        
   
    def execute(self, cursor):
        query_formated = self.query.format(schema_name = self.schema_name, table_name = self.table_name)

        negative_words = [
        'Office', 
        'Office 365', 
        'SQL', 
        'Windows', 
        'Adobe', 
        'Autocad', 
        'CorelDraw',
        'Power', 
        'VMware', 
        'vSphere', 
        'Copilot', 
        'Autodesk', 
        'Acrobat', 
        'Revit', 
        'Acquia', 
        'ARCHITECTURE', 
        'DYNAMICS', 
        'Creative', 
        'E-Mobility',
        'BPO'  
        ]
      
    
        conditions = " OR ".join([f"descricao ILIKE %s" for _ in negative_words])
        
        final_query = query_formated.replace("conditions", conditions)

    
        params = [f'%{word}%' for word in negative_words]
       
        
        cursor.execute(final_query, params)
        print(cursor.statusmessage)








        


    





  




            









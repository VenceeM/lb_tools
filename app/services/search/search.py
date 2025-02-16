from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text
from app.schemas.tantivy.schema import schema
import tantivy
from typing import List
from fastapi import HTTPException,status
from collections import OrderedDict
import os
import tempfile
import shutil

class SearchService:
    dir = f"{os.getcwd()}/tmp/temp_index"
    def __init__(self):
        self.schema_builder =  tantivy.SchemaBuilder()
        self.index:tantivy.Index = None
        self.schema:tantivy.Schema = None
        
        
    async def init_data(self,data:List[dict]):
      
        try: 
            
            if os.path.exists(f"{self.dir}/meta.json"):
                shutil.rmtree(self.dir)
                os.makedirs(self.dir,exist_ok=True)
                
            
            keys = set()
            for item in data:
                keys.update(item.keys())
        
                
            for key in keys: 
                self.schema_builder.add_text_field(f"{key}",stored=True,tokenizer_name="en_stem")
            
            self.schema = self.schema_builder.build()
            self.index = tantivy.Index(schema=self.schema,path=dir)
                    
            writer = self.index.writer()
            
            for item in data:
                
                writer.add_document(
                    tantivy.Document(
                        **{key:item.get(key,"") for key in keys}
                    )
                )
                
            writer.commit()
            writer.wait_merging_threads()
            
            return {"message":"Initialize Successfully"}
        except Exception as e:

            raise(HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}"
            ))
        
    def checker(self) -> bool:
        if os.path.exists(f"{os.getcwd()}/tmp/temp_index/meta.json"):
            self.index = tantivy.Index.open(f"{os.getcwd()}/tmp/temp_index")
            return True
        elif not os.path.exists(f"{os.getcwd()}/tmp/temp_index/meta.json"):
            return False
            
        if self.index is None:
            return False
        
    async def search(self,query:str,field_names:list[str]):
        
      
        if "" in field_names:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please input a field names eg: (lastname name id)."
            )
        
        if not self.checker():
            return {"result":"No records"}
        
        self.index.reload()
        searcher = self.index.searcher()
        parse_query = self.index.parse_query(query,field_names)
        result = searcher.search(parse_query,100)
        
        hits = []
        default = []
        
        if query:
            for score, doc_address in result.hits:
                doc = searcher.doc(doc_address=doc_address)
                
                doct_dict = {field:doc[field][0] for field in doc.to_dict()}
            
                hits.append(doct_dict)
            return {"results":hits}
  

        for doc_id in range(searcher.num_docs):
            doc_address = tantivy.DocAddress(doc_id, 0)

            doc = searcher.doc(doc_address=doc_address)
            
            default.append({field:doc[field][0] for field in doc.to_dict()})

        
            
        default.sort(key=lambda x: x["id"], reverse=False)
        return {"results":default}  
    
    
    async def add_or_update(self, item:dict):
        
        self.checker()
        
        if not "id" in item:
            return {"result":"Error"}
        

        query = f"id:{item["id"]}"
        searcher = self.index.searcher()
        writer = self.index.writer()
        results = searcher.search(self.index.parse_query(query, ["id"]),1) 
        
        if results.hits:
            writer.delete_documents(
                "id",
                item["id"]
            )
            
        writer.add_document(
            tantivy.Document(
                ** {key: item.get(key,"") for key in item}
            )
        )
        
        writer.commit()
        writer.wait_merging_threads()
        
        return {"result":"Successfull"}
        
    
    async def delete_all_records(self):
        
        self.checker()
        
        writer = self.index.writer()
        
        writer.delete_all_documents()
        
        writer.commit()
        
        return {"result:sucessfull"}
        
    
    
    
    
   
        
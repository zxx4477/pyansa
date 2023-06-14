# -*- coding: utf-8 -*-
"""
Created on Mon May 29 15:18:36 2023

@author: xinxing.zhang
"""
import os
import ansa
import numpy as np
from ansa import base
from ansa import constants
import sqlite3
import csv


class MaterialLibrary(object):
	
    ## Construct a Material Library Class
    # @param None
    def __init__(self):
        self.mat_db_name = "material";
        self.mat_tab_name = "material_id_manager";
        self.mat_data_name = "Material_Name_ID_Manager.csv"
        self.fp_db = os.path.join(os.path.dirname(__file__),self.mat_db_name+'.db');
        self.fp_csv = os.path.join(os.path.dirname(__file__),self.mat_data_name);
    
    #
    def helpinfo(self):
        print("""
              =========================================================================================================================== 
              Usage: 
                  The MaterialLibrary Class can be used to query material info.
              Author: 
                  Xinxing.Zhang
              Common commands listed as below:  
                  matlib = MaterialLibrary();
                  matlib.querySqlTableNames(); # Get table names in database
                  matlib.querySqlTablekeys(); # Get keys of material table
                  matlib.QueryMaterialNames(); # Get All matetial names in teamcenter
                  matlib.QueryMaterialAllInfo("Si10Mg"); # Get material's all info by material_tc_name
                  matlib.QueryMaterialSingleInfo("Si10Mg","CAE_NAME"); # Get material's CAE_NAME by material_tc_name
                  matlib.QueryMaterialSingleInfo("Si10Mg","NASTRAN_ID"); # Get material's NASTRAN_ID by material_tc_name
              =========================================================================================================================== 
              """)    
    
    # Create material database (sqlite format)
    def createSqlTable(self):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor();
        sql = f'''
            CREATE TABLE {self.mat_tab_name}(
                TC_ID varchar(20) NULL,
                TC_NAME varchar(50) NULL,
                CAE_NAME varchar(50) NULL,
                DYNA_ID varchar(11) NULL,
                NASTRAN_ID varchar(11) NULL,
                ABAQUS_ID varchar(11) NULL,
                E FLOAT NULL,
                NU FLOAT NULL,
                RHO varchar(20) NULL
                );
        '''
        cursor.execute(sql)
        cursor.close()
        conn.close()
    
    #
    def cleanAllTableData(self):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor(); 
        sql = f'delete from {self.mat_tab_name};';
        cursor.execute(sql);
        conn.commit();
        cursor.close();
        conn.close();

    #
    def importDataToSqlite(self):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor(); 
        with open(self.fp_csv,'r') as f:
            for row in csv.reader(f, skipinitialspace=True):
                if row[0] != "" and row[0] != "TC_ID":
                    tc_id = row[0];
                    tc_name = row[1];
                    cae_name = row[2];
                    dyna_id = row[3];
                    nastran_id = row[4];
                    abaqus_id = row[5];
                    e = row[6];
                    if e == "": 
                        e=0.0;
                    else:
                        e = float(e);
                    nu = row[7];
                    if nu == "": 
                        nu=0.0;
                    else:
                        nu = float(nu);
                    rho = row[8];
                    if rho == "": 
                        rho="0.0";
                    else:
                        rho = str(rho);
                    sql = f'INSERT INTO {self.mat_tab_name} (TC_ID, TC_NAME, CAE_NAME,DYNA_ID,NASTRAN_ID,ABAQUS_ID,E,NU,RHO) VALUES ("{tc_id}", "{tc_name}", "{cae_name}","{dyna_id}","{nastran_id}","{abaqus_id}","{e}","{nu}","{rho}");' 
                    print(sql);
                    cursor.execute(sql);
                    conn.commit();
        conn.commit();
        f.close();
        cursor.close();
        conn.close();

    #
    def querySqlTableNames(self):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor();
        cursor.execute('select name from sqlite_master where type="table"')
        tab_name=cursor.fetchall();
        cursor.close()
        conn.close()  
        return [line[0] for line in tab_name]

    #
    def querySqlTablekeys(self):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor();
        sql = 'pragma table_info(material_id_manager);';
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close() 
        return [line[1] for line in res]

    #  
    def QueryMaterialNames(self):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor();
        sql_query = 'select TC_NAME from material_id_manager;';
        cursor.execute(sql_query);
        result_tuple = cursor.fetchall();
        cursor.close();  
        conn.close();  
        return [i[0] for i in result_tuple]

    # 
    def QueryMaterialAllInfo(self,tc_name):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor();
        sql_query = f'select * from material_id_manager where TC_NAME="{tc_name}"';
        cursor.execute(sql_query);
        result_tuple = cursor.fetchall();
        cursor.close();  
        conn.close(); 
        if result_tuple:
            result_list = list(result_tuple[0]);
            return result_list;
        else:
            return [];
         
    #  
    def QueryMaterialSingleInfo(self,tc_name,label):
        conn = sqlite3.connect(self.fp_db);
        cursor = conn.cursor();
        sql_query = f'select {label} from material_id_manager where TC_NAME="{tc_name}"';
        cursor.execute(sql_query);
        result_tuple = cursor.fetchall();
        cursor.close();  
        conn.close();  
        if result_tuple:
            result = result_tuple[0][0];
            return str(result);
        else:
            return "";

#
if __name__=="__main__":
    matlib =MaterialLibrary();
    matlib.createSqlTable();
    matlib.cleanAllTableData();
    matlib.importDataToSqlite();
    matlib.helpinfo()
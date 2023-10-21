import sys
import cdsapi
import os
from google.cloud import storage
from zipfile import ZipFile
#from ExtraccionZip import readzip


bucket_name = 'dmc-proyecto-big-data-24'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/var/lib/jenkins/workspace/proyecto-big-data-24-2ba1fba24bbb.json'
storage_client = storage.Client()
# Accediendo al bucket
bucket_proyecto = storage_client.get_bucket('dmc-proyecto-big-data-24')


def descomprimir(path_zip, name, path_file):
    file_zip = os.path.join(path_zip , name)
    name = name.split('.')[0]
    with ZipFile(file_zip, 'r') as obj_zip:
        FileNames = obj_zip.namelist()
        for fileName in FileNames:
            count_file = 0
            if fileName.endswith('.nc'):
                count_file = count_file +1
                obj_zip.extract(fileName, path_file)
                os.rename(path_file + '/' + fileName, path_file + '/' +str(count_file) + name + '.nc')
                print("==> Archifo %s extraido"%count_file + name + '.nc')


#Funcion que envia el archivo a cloud Storage
def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False
    

#Funcion que elimina archivo en cloud Storage    
def delete_blob(bucket_name, blob_name):    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None
    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation
    blob.delete(if_generation_match=generation_match_precondition)
    print(f"Blob {blob_name} deleted.")


def main(arg):
    list_variable = ["cloud_cover","snow_thickness_lwe","2m_temperature","2m_dewpoint_temperature","snow_thickness","vapour_pressure","10m_wind_speed"]
    check_month = int(arg[1])
    check_year = int(arg[2])
    check_variable = arg[3]
    if not(check_month < 13 and check_month > 0):
        return "El mes debe estar entre 1 y 12"       
    if not(check_year < 2024 and check_year > 2017):
        return "El año debe estar entre 2018 y 2023"
    if check_variable not in list_variable:
        return "La variable debe ser una de las siguientes: cloud_cover,snow_thickness_lwe,2m_temperature,2m_dewpoint_temperature,snow_thickness,vapour_pressure,10m_wind_speed"
    month = arg[1]
    year = arg[2]
    variable = arg[3]
    c = cdsapi.Client()
    file_cdsapi = 'CDSAPI-' + variable + '-' + year + '-' + month
    file_cdsapi_zip = file_cdsapi + '.zip'
    path_zip = './DataZip'
    path_file = './Data'
    if not os.path.exists(path_zip):
        os.mkdir(path_zip)

    if not os.path.exists(path_file):
        os.mkdir(path_file)   
        
    c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'version': '1_1',
            'format': 'zip',
            'statistic': '24_hour_mean',
            'area': [
                0, -81, -18,
                -69,
            ],
            'month': month,
            'day': '01',
            'year': year,
            'variable': variable,
        },
        os.path.join(path_zip , file_cdsapi_zip))
    
    path_bucket = 'datalake/workload/cdsapi/' + variable + '/'

    descomprimir(path_zip,file_cdsapi_zip, path_file)

    #Envio de archivos a la capa Workload
    #Cargar Archivos
    blobs = storage_client.list_blobs(bucket_name)

    files_nc = os.listdir(path_file)

    for fileName in files_nc:                   
        upload_to_bucket(path_bucket + fileName, os.path.join(path_file, fileName), bucket_name)  
        os.remove(os.path.join(path_file, fileName))
        if fileName in blobs:
            delete_blob(bucket_name, path_bucket + fileName) 
    
    files_zip = os.listdir(path_zip)           
    for fileName in files_zip:
        os.remove(os.path.join(path_zip, fileName))


if __name__ == '__main__' and len(sys.argv) == 4:
    main(sys.argv)
    

from pyspedas.mms.mms_login_lasp import mms_login_lasp
from shutil import copyfileobj, copy
from tempfile import NamedTemporaryFile
from pyspedas.mms.mms_config import CONFIG
import os

def eva_get_selections_file(type='abs_selections',start_date='2023-08-10',end_date='2023-08-11',latest=False):
  """
  Get ABS and SITL files

  Parameters
  ----------
      type : str
          indicates which type file to download, valide values are 'abs_selections' and 'sitl_selections'

      start_date: str
          start date of the period from which the ABS/SITL files are searched

      end_date: str
          end date of the period from which the ABS/SITL files are searched

      latest: bool
          If True, the latest ABS/SITL file be retrieved. The default is False.

  Returns
  ----------
      List of retrieved ABS or SITL files

  """
  #---------------
  # INITIALIZE
  #---------------
  headers = {}
  out_files = []
  sdc_session, user = mms_login_lasp(always_prompt=False)
  if latest == True:
    start_date = ""
    end_date   = ""

  #---------------
  # GET FILE NAMES
  #---------------
  url = "https://lasp.colorado.edu/mms/sdc/public/files/api/v1/file_info/" + type
  if len(start_date) > 0:
    url = url + "?start_date="+start_date
  if len(end_date) > 0:
    url = url + "&end_date="+end_date
  fsrc_json = sdc_session.get(url, stream=True, verify=True, headers=headers).json()

  # -------------------------
  # GET EACH FILE
  # -------------------------
  for file in fsrc_json['files']:

    # Prep for output 
    file_name = file['file_name']
    yyyy = ((file_name.split('_'))[2])[0:4]
    out_dir  = os.sep.join([CONFIG['local_data_dir'], 'sitl', type, yyyy])
    if not os.path.exists(out_dir):
      os.makedirs(out_dir)
    out_file = os.sep.join([out_dir, file['file_name']])

    # Get the file
    url = "https://lasp.colorado.edu/mms/sdc/public/files/api/v1/download/" + type
    url = url + "?file="+file_name
    fsrc = sdc_session.get(url, stream=True, verify=True, headers=headers) # fetch the file from SDC
    ftmp = NamedTemporaryFile(delete=False) # create a temporary file
    with open(ftmp.name, 'wb') as f:
      copyfileobj(fsrc.raw, f) # save the fetched object into the temporary file
    copy(ftmp.name, out_file) # copy the temporary file to the destination location.
    fsrc.close()
    ftmp.close()

    # Add to the list
    out_files.append(out_file)

  return out_files

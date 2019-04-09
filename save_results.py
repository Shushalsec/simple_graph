import os
import shutil
import datetime

if __name__ == '__main__':

    # SETUP THE DIRECTORIES FOR COPYING TO AND FROM
    HIST_DIR = r'M:\ged-shushan\ged-shushan\data\Histology'
    ged_results_dir = r'M:\ged-shushan\ged-shushan\results-shushan'
    ged_src_dir = os.path.join(HIST_DIR, 'data_for_GED')

    result_dir = r'M:\EXPERIMENT_RESULTS'
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)
    # project_dir = os.getcwd()
    project_dir = r'M:\pT1_selected - template_annotated - QuPath_export_cell'

    experiment_name = os.path.basename(os.path.normpath(project_dir))
    currentDT = datetime.datetime.now()
    time = str(currentDT)
    time = time.replace(':', '').replace('.', '')
    # to save the version information create a folder with the result folder name + datetime stamp
    new_dir = os.path.join(result_dir, 'EXPERIMENT_'+experiment_name + '_' + time)
    os.mkdir(new_dir)

    #COPY QUPATH DATA
    file_name = [file for file in os.listdir(os.path.join(project_dir, 'scripts')) if file.endswith('.groovy')][0]
    shutil.copy(os.path.join(project_dir, 'scripts', file_name), new_dir)
    shutil.copy(os.path.join(project_dir, 'parameters.txt'), new_dir)
    shutil.copy(os.path.join(project_dir, 'project.qpproj'), new_dir)
    shutil.copytree(os.path.join(project_dir, 'data'), os.path.join(new_dir, 'data'))

    # COPY GED RESULTS AND PARAMETERS
    shutil.copytree(ged_src_dir, os.path.join(new_dir, 'data_for_GED'))
    shutil.copytree(ged_results_dir, os.path.join(new_dir, 'results-shushan'))
    shutil.copy(r'M:\ged-shushan\ged-shushan\properties\letters-hed.prop', os.path.join(new_dir, 'letters-hed.prop'))


    #CLEANUP OF THE Histology folder
    shutil.rmtree('M:\ged-shushan\ged-shushan\data\Histology\data_for_GED')

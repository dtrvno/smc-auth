version=1.0
uploaded_status="UPLOADED"
running_status="RUNNING"
failing_status="FAILED"
succeed_status="SUCCEEDED"
SMC_CONFIGURATION_ENVIRONMENT="SMC_ORCHESTRATOR_CONFIGURATION"
LOGGER_NAME="smc-orchestrator"
STEP_STATUS_SUCCEED="succeeded"
STEP_STATUS_FAILED="failed"
STEP_STATUS_RUNNING="running"
STEP_STATUS_TIMEOUT="timeout"
STEP_STATUS_SKIPPED="skipped"
CONFIGURATION_ID="payload_id"
HARDWARE_JSON_FORMAT="{0}_hardware.json"
UPLOAD_ACTIVITY="upload"
DEPLOY_ACTIVITY="deploy"
RESET_ACTIVITY="reset"
VALIDATE_ACTIVITY="validate"
BOOTSTRAP_ACTIVITY="bootstrap"
INSTALL_OS="install_os"
SET_NETWORK_ACTIVITY = "setNetwork"
UPLOAD_ACTIVITY_MESSAGE="Configuration uploaded"
DEPLOY_ACTIVITY_MESSAGE="Configuration deployed"
SUPPORTED_VERBS=["deploy","reset","validate","bootstrap","setNetwork"]
FILLED_ATTRIBUTE="need to be filled"
WORKING_DIR="/tmp/ceph"
WIN_WORKING_DIR="c:\\smc"
PAYLOAD_DIR = "payload"
ETC_PORTION_FILE_NAME="etc_portion.txt"
ANSIBLE_HOST_FILE_NAME="hosts"
SSH_CONFIG_FILE_NAME="config"
CENTOS="centos"
UBUNTU="ubuntu"
INSTALL_OS_RUNNING="Install OS running"
INSTALL_OS_FINISHED_WITH_ERRORS="Install OS finished with errors"
INSTALL_OS_FINISHED_SUCCESS="Install OS finished successfully"
VALIDATE_STATUS_FILE = "validate.json"
BOOTSTRAP_STATUS_FILE = "bootstrap.json"
SET_NETWORK_STATUS_FILE = "setNetwork.json"
SOLUTION_CONFIG_FILE="solution_config.json"
SOLUTION_SPEC_FILE="solution_spec.json"
NODES_FILE = "nodes.json"
NODE_ACTIVITIES = [BOOTSTRAP_ACTIVITY, SET_NETWORK_ACTIVITY]
NODE_CONFIG_FILES = [VALIDATE_STATUS_FILE, BOOTSTRAP_STATUS_FILE, SET_NETWORK_STATUS_FILE]



#!/bin/bash

required_environment_variables=("DMTIME_DB_URI" "DMTIME_DB_USER" "DMTIME_DB_PW" "DMTIME_JWT_KEY" "DMTIME_IMAGE_STORAGE" "DMTIME_SERVER_NAME")



verify_required_env() {
    for require_var_name in "${required_environment_variables[@]}"; do
        
        if [ -z $(printenv $require_var_name) ]; then
            printf '%s is not found. Check environment.\n' $require_var_name
            exit 1
        fi
    done
}       

verify_required_env
uwsgi -i DMInside.ini
# cmake file to trigger hipify

cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

set(HIPIFY_DICT_FILE ${CMAKE_BINARY_DIR}/hipify_output_dict_dump.txt)
set(_temp_file_cuda_to_hip_list "cuda_to_hip_list")

# Get the hipify_cli.py source directory from current directory by going to parent directory
get_filename_component(HIPIFY_DIR ${CMAKE_CURRENT_LIST_DIR} DIRECTORY)

function(write_file_list FILE_SUFFIX INPUT_LIST)
  message(STATUS "Writing ${FILE_SUFFIX} into file - file_${FILE_SUFFIX}.txt")
  set(_FULL_FILE_NAME "${CMAKE_BINARY_DIR}/${_temp_file_cuda_to_hip_list}_${FILE_SUFFIX}.txt")
  file(WRITE ${_FULL_FILE_NAME} "")
  foreach(_SOURCE_FILE ${INPUT_LIST})
    file(APPEND ${_FULL_FILE_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/${_SOURCE_FILE})
    file(APPEND ${_FULL_FILE_NAME} "\n")
  endforeach()
endfunction()

function(get_file_list FILE_SUFFIX OUTPUT_LIST)
  set(_FULL_FILE_NAME "${CMAKE_BINARY_DIR}/${_temp_file_cuda_to_hip_list}_${FILE_SUFFIX}.txt")
  file(STRINGS ${_FULL_FILE_NAME} _FILE_LIST)
  set(${OUTPUT_LIST}_HIP ${_FILE_LIST} PARENT_SCOPE)
endfunction()

function(update_list_with_hip_files FILE_SUFFIX)
  set(_SCRIPTS_DIR ${HIPIFY_DIR}/tools)
  set(_FULL_FILE_NAME "${CMAKE_BINARY_DIR}/${_temp_file_cuda_to_hip_list}_${FILE_SUFFIX}.txt")
  set(_EXE_COMMAND
    ${_SCRIPTS_DIR}/replace_cuda_with_hip_files.py
    --io-file ${_FULL_FILE_NAME}
    --dump-dict-file ${HIPIFY_DICT_FILE})
  execute_process(
    COMMAND ${_EXE_COMMAND}
    RESULT_VARIABLE _return_value)
  if (NOT _return_value EQUAL 0)
    message(FATAL_ERROR "Failed to get the list of hipified files!")
  endif()
endfunction()

function(get_hipified_list INPUT_LIST OUTPUT_LIST)
  string(RANDOM LENGTH 16 RAND_STRING)
  set(TEMP_FILE_NAME "tmp_${RAND_STRING}")
  file(REMOVE ${TEMP_FILE_NAME})

  write_file_list("${TEMP_FILE_NAME}" "${INPUT_LIST}")
  update_list_with_hip_files("${TEMP_FILE_NAME}")
  get_file_list("${TEMP_FILE_NAME}" __temp_srcs)

  set(${OUTPUT_LIST} ${__temp_srcs_HIP} PARENT_SCOPE)
endfunction()

set(HIPIFY_COMMAND
  ${HIPIFY_DIR}/hipify_cli.py
  --project-directory ${PROJECT_SOURCE_DIR}
  --output-directory ${PROJECT_SOURCE_DIR}
  --dump-dict-file ${HIPIFY_DICT_FILE}
)

execute_process(
  COMMAND ${HIPIFY_COMMAND}
  RESULT_VARIABLE hipify_return_value
)
if (NOT hipify_return_value EQUAL 0)
  message(FATAL_ERROR "Failed to hipify files!")
endif()


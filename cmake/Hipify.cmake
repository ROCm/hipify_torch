# cmake file to trigger hipify

# Get the hipify_cli.py source directory from current directory
get_filename_component(HIPIFY_SCRIPTS_DIR ${CMAKE_CURRENT_LIST_DIR} DIRECTORY)
set(HIPIFY_COMMAND
  ${HIPIFY_SCRIPTS_DIR}/hipify_cli.py
  --project-directory ${PROJECT_SOURCE_DIR}
  --output-directory ${PROJECT_SOURCE_DIR}
)

execute_process(
  COMMAND ${HIPIFY_COMMAND}
  RESULT_VARIABLE hipify_return_value
)
if (NOT hipify_return_value EQUAL 0)
  message(FATAL_ERROR "Failed to hipify files!")
endif()


#
# project: assignments
#
cmake_minimum_required(VERSION 2.8)
get_filename_component(FIPS_ROOT_DIR "../fips" ABSOLUTE)
include("${FIPS_ROOT_DIR}/cmake/fips.cmake")

set(ORYOL_SAMPLE_URL "http://floooh.github.com/oryol-samples/data/" CACHE STRING "Samples URL" FORCE)

include_directories(src)

fips_setup()
fips_project(assignments)
fips_add_subdirectory(src)
fips_finish()



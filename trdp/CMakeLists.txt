cmake_minimum_required(VERSION 3.10)
project(TRDP C)

if (MSVC)
  #set(TARGET_OS "windows") # Some weird detection in the source
  set(TARGET_VOS "windows")
elseif(UNIX)
  set(TARGET_OS "POSIX")
  set(TARGET_VOS "posix")
elseif(VXWORKS)
  set(TARGET_OS "VXWORKS")
  set(TARGET_VOS "vxworks")
else()
  message(FATAL_ERROR "Unsupported target OS")
endif()

add_compile_definitions(TARGET_OS="${TARGET_OS}")

option(MD_SUPPORT "Enable / disable MD support" ON)
option(FULL_BUILD "Full build with TRDP optional files" ON)

set(INCLUDE_PATH ${INCLUDE_PATH} src/api)
set(TARGET_SPECIFIC_VOS_INCLUDE_PATH ${TARGET_SPECIFIC_VOS_INCLUDE_PATH} src/vos/${TARGET_VOS})
set(VOS_INCLUDE_PATH ${VOS_INCLUDE_PATH} src/vos/api src/common)

set(INCLUDE_PATHS_FULL ${INCLUDE_PATH} ${TARGET_SPECIFIC_VOS_INCLUDE_PATH} ${VOS_INCLUDE_PATH})

# FLINT binary path
set(FLINT ${LINT_BINPATH}flint)

# Set LINT Objects
set(LINT_OBJECTS 
  trdp_stats.lob
  vos_utils.lob
  vos_sock.lob
  vos_mem.lob
  vos_thread.lob
  vos_shared_mem.lob
  trdp_pdcom.lob
  trdp_mdcom.lob
  trdp_utils.lob
  tlc_if.lob
  tlp_if.lob
  tlm_if.lob
  trdp_stats.lob
)

# Enable / disable MD Support
# by default MD_SUPPORT is always enabled (in current state)
if(MD_SUPPORT)
  set(CFLAGS ${CFLAGS} -DMD_SUPPORT=0)
else()
  set(TRDP_OBJS ${TRDP_OBJS} trdp_mdcom.o tlm_if.o)
  set(CFLAGS ${CFLAGS} -DMD_SUPPORT=1)
endif()

# Check for RT_THREADS
if (RT_THREADS)
  add_compile_definitions(RT_THREADS=1)
endif ()

set (VOS_C_FILES
    src/vos/common/vos_utils.c
    src/vos/common/vos_mem.c
    src/vos/${TARGET_VOS}/vos_sock.c
    src/vos/${TARGET_VOS}/vos_thread.c
    src/vos/${TARGET_VOS}/vos_shared_mem.c
)

set(TRDP_C_FILES
    src/common/trdp_pdcom.c
    src/common/trdp_utils.c
    src/common/tlp_if.c
    src/common/tlc_if.c
    src/common/trdp_stats.c
)

# Check for MD_SUPPORT
if (MD_SUPPORT)
  set(TRDP_C_FILES ${TRDP_C_FILES} src/common/trdp_mdcom.c src/common/tlm_if.c)
  add_definitions(-DMD_SUPPORT=1)
else ()
  add_definitions(-DMD_SUPPORT=0)
endif ()

if (FULL_BUILD)
  set(TRDP_OPT_C_FILES
      src/common/trdp_xml.c
      src/common/tau_xml.c
      src/common/tau_marshall.c
      src/common/tau_dnr.c
      src/common/tau_tti.c
      src/common/tau_ctrl.c
  )
endif ()

# Check for SOA_SUPPORT
if (SOA_SUPPORT)
  if (FULL_BUILD)
    set(TRDP_OPT_C_FILES ${TRDP_OPT_C_FILES} src/common/tau_so_if.c)
  endif ()
  add_compile_definitions(SOA_SUPPORT=1)
else ()
  add_compile_definitions(SOA_SUPPORT=0)
endif ()

# Add the targets
add_library(trdp STATIC ${VOS_C_FILES} ${TRDP_C_FILES} ${TRDP_OPT_C_FILES})
target_include_directories(trdp PUBLIC ${INCLUDE_PATHS_FULL})

install(TARGETS trdp DESTINATION lib)
set(srcs "test_app_main.c"
         "test_dac.c")

if(CONFIG_DAC_ISR_IRAM_SAFE)
    list(APPEND srcs "test_dac_iram.c")
endif()

# In order for the cases defined by `TEST_CASE` to be linked into the final elf,
# the component can be registered as WHOLE_ARCHIVE
idf_component_register(SRCS ${srcs}
                       PRIV_REQUIRES unity esp_driver_pcnt driver esp_adc
                       WHOLE_ARCHIVE)

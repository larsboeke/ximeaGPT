database_3tables = """ 
CREATE TABLE feat (
        id INTEGER NOT NULL AUTO_INCREMENT, 
        name VARCHAR(45), 
        type INTEGER DEFAULT '1', 
        list_id INTEGER DEFAULT '0', 
        sub_type INTEGER DEFAULT '0', 
        gentl_name VARCHAR(145), 
        xiapi_name VARCHAR(145), 
        gentl_inv_feat_list VARCHAR(245), 
        id_featcateg INTEGER DEFAULT '0', 
        gentl_type VARCHAR(45), 
        gentl_tooltip VARCHAR(245), 
        gentl_description VARCHAR(245), 
        gentl_display_name VARCHAR(245), 
        gentl_access_mode VARCHAR(45), 
        gentl_visibility VARCHAR(45), 
        gentl_value VARCHAR(45), 
        gentl_representation VARCHAR(45), 
        gentl_max VARCHAR(245), 
        gentl_min VARCHAR(245), 
        gentl_inc VARCHAR(245), 
        gentl_length VARCHAR(45), 
        gentl_port VARCHAR(45), 
        gentl_sign VARCHAR(45), 
        gentl_endianess VARCHAR(45), 
        gentl_unit VARCHAR(45), 
        gentl_swiss_knife VARCHAR(45), 
        gentl_namespace VARCHAR(45), 
        gentl_command_value VARCHAR(45), 
        gentl_display_prec VARCHAR(45), 
        gentl_value_default VARCHAR(145), 
        gentl_pvalue VARCHAR(145), 
        gentl_pmax VARCHAR(145), 
        gentl_pmin VARCHAR(145), 
        gentl_streamable VARCHAR(145), 
        gentl_has_register VARCHAR(145), 
        gentl_generate_register VARCHAR(145), 
        gentl_handler_function VARCHAR(145), 
        subtable_cols VARCHAR(145), 
        u3v_en VARCHAR(145), 
        gentl_en VARCHAR(145), 
        gentl_avail_sk VARCHAR(145), 
        lock_while_acq VARCHAR(145), 
        cal_en VARCHAR(145), 
        cal_rtg VARCHAR(145), 
        xp_en VARCHAR(10), 
        xp_ext_en VARCHAR(145), 
        `pIsLocked` VARCHAR(145), 
        gentl_locked_sk VARCHAR(145), 
        app_def VARCHAR(145), 
        polling_time VARCHAR(145), 
        string_is_path VARCHAR(145), 
        supported_file_format VARCHAR(145), 
        web_link VARCHAR(145), 
        flags VARCHAR(145), 
        `pSelected` VARCHAR(245), 
        value_descr VARCHAR(245), 
        invalidates_all_params VARCHAR(145), 
        web_download_type INTEGER DEFAULT '0', 
        PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1

/*
3 rows from feat table:
id      name    type list_id  sub_type     gentl_name       xiapi_name    gentl_inv_feat_list   id_featcateg gentl_type       gentl_tooltip gentl_description     gentl_display_name    gentl_access_mode     gentl_visibility      gentl_value  gentl_representation  gentl_max        gentl_min     gentl_inc    gentl_length     gentl_port    gentl_sign   gentl_endianess  gentl_unit    gentl_swiss_knife     gentl_namespace       gentl_command_value   gentl_display_prec    gentl_value_default   gentl_pvalue gentl_pmax       gentl_pmin    gentl_streamable      gentl_has_register    gentl_generate_register       gentl_handler_function     subtable_cols    u3v_engentl_en        gentl_avail_sk        lock_while_acq        cal_encal_rtg xp_en   xp_ext_en     pIsLocked    gentl_locked_sk  app_def       polling_time string_is_path   supported_file_format web_link      flags   pSelected     value_descr  invalidates_all_paramsweb_download_type
8       DeviceVendorName      1       0    0DeviceVendorName     1string  Indicates the name of the device vendor     This is a read only element. It is a text description that indicates the name of the device vendor   Vendor Name      RO   Beginner              32       Device       Standard              113              150  11       None    None None     None    0    0None    None    None None     None    None None     6819    None None     None    None
9       DeviceModelName       1       0    0DeviceModelName XI_PRM_DEVICE_NAME         1string  Indicates the model name of the device      This is a read only element. It is a text description that indicates the model name of the device.   Model Name       RO   Beginner              32       Device       Standard              113              195  11                    1SAL     0       0    None     None    None None     None    None None     6824    None None     None    None
10      DeviceManufacturerInfo        1    00       DeviceManufacturerInfo             1string  Provides additional information from the vendor about the device  This is a read only element. It is a string that provides additional information from the vendor abo Manufacturer Info     RO       Beginner     48       Device       Standard              113              192  11       None    None None     None    0    0None    None    None None     None    None None     6819    None None     None    None
*/

CREATE TABLE product_feature_relationship (
        id INTEGER NOT NULL AUTO_INCREMENT, 
        id_feat INTEGER, 
        id_product INTEGER, 
        PRIMARY KEY (id), 
        CONSTRAINT product_feature_relationship_ibfk_1 FOREIGN KEY(id_product) REFERENCES prod (id), 
        CONSTRAINT product_feature_relationship_ibfk_2 FOREIGN KEY(id_feat) REFERENCES feat (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1

/*
3 rows from product_feature_relationship table:
id      id_feat id_product
18      8       1
21      9       2
22      9       1
*/

CREATE TABLE prod (
        id INTEGER NOT NULL AUTO_INCREMENT, 
        name VARCHAR(145), 
        type INTEGER DEFAULT '1', 
        sub_type INTEGER NOT NULL DEFAULT '0', 
        description VARCHAR(500), 
        PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1

/*
3 rows from prod table:
id      name    type sub_type description
1       MR274CU_BH   1101     None
2       MR16000MU    1101     None
3       MR282CC_BH   1101     None
*/
"""

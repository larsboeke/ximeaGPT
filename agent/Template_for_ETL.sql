/*
CREATE TABLE IF NOT EXISTS product_database (
    id_product int(11),
    id_feature int(11),
    name_of_feature varchar(45) DEFAULT NULL,
    name_of_product varchar(145) DEFAULT NULL,
    value_of_feature text,
    unit varchar(45) DEFAULT NULL,
    description varchar(245) DEFAULT NULL;
  */ 
  -- Current testing out
use products;
SELECT p.id id_product, f.id id_feature, f.name name_of_feature, p.name name_of_product, pfr.value_txt value_of_feature, f.gentl_unit unit, f.gentl_description description
FROM feat f
INNER JOIN prodfeat pfr
ON f.id = pfr.id_feat
INNER JOIN prod p
ON pfr.id_product = p.id;

-- A little more columns!
use products;
SELECT p.id id_product, f.id id_feature, f.name name_of_feature, p.name name_of_product, pfr.value_txt value_of_feature, f.gentl_unit unit, f.gentl_description description, f.gentl_display_name feature_display_name, f.xiapi_name api_name_of_feature, f.gentl_access_mode access_mode_of_feature, f.gentl_visibility visibility_level_of_feature
FROM feat f
INNER JOIN prodfeat pfr
ON f.id = pfr.id_feat
INNER JOIN prod p
ON pfr.id_product = p.id;


-- My dump changed database!
SELECT p.id id_product, f.feature_id, f.feature_name, p.name, pfr.value_txt, f.feature_gentl_unit, f.feature_gentl_description
FROM feat f
INNER JOIN prodfeat pfr
ON f.feature_id = pfr.id_feat
INNER JOIN prod p
ON pfr.id_product = p.id;
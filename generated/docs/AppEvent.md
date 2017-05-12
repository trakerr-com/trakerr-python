# AppEvent

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | API key generated for the application | 
**log_level** | **str** | (optional) Logging level, one of &#39;debug&#39;,&#39;info&#39;,&#39;warning&#39;,&#39;error&#39;, &#39;fatal&#39;, defaults to &#39;error&#39; | [optional] 
**classification** | **str** | (optional) one of &#39;issue&#39; or a custom string for non-issues, defaults to &#39;issue&#39; | 
**event_type** | **str** | type of the event or error (eg. NullPointerException) | 
**event_message** | **str** | message containing details of the event or error | 
**event_time** | **int** | (optional) event time in ms since epoch | [optional] 
**event_stacktrace** | [**Stacktrace**](Stacktrace.md) |  | [optional] 
**event_user** | **str** | (optional) event user identifying a user | [optional] 
**event_session** | **str** | (optional) session identification | [optional] 
**context_app_version** | **str** | (optional) application version information | [optional] 
**deployment_stage** | **str** | (optional) deployment stage, one of &#39;development&#39;,&#39;staging&#39;,&#39;production&#39; or a custom string | [optional] 
**context_env_name** | **str** | (optional) environment name (like &#39;cpython&#39; or &#39;ironpython&#39; etc.) | [optional] 
**context_env_language** | **str** | (optional) language (like &#39;python&#39; or &#39;c#&#39; etc.) | [optional] 
**context_env_version** | **str** | (optional) version of environment | [optional] 
**context_env_hostname** | **str** | (optional) hostname or ID of environment | [optional] 
**context_app_browser** | **str** | (optional) browser name if running in a browser (eg. Chrome) | [optional] 
**context_app_browser_version** | **str** | (optional) browser version if running in a browser | [optional] 
**context_app_os** | **str** | (optional) OS the application is running on | [optional] 
**context_app_os_version** | **str** | (optional) OS version the application is running on | [optional] 
**context_data_center** | **str** | (optional) Data center the application is running on or connected to | [optional] 
**context_data_center_region** | **str** | (optional) Data center region | [optional] 
**context_tags** | **list[str]** |  | [optional] 
**context_url** | **str** | (optional) The full URL when running in a browser when the event was generated. | [optional] 
**context_operation_time_millis** | **int** | (optional) duration that this event took to occur in millis. Example - database call time in millis. | [optional] 
**context_cpu_percentage** | **int** | (optional) CPU utilization as a percent when event occured | [optional] 
**context_memory_percentage** | **int** | (optional) Memory utilization as a percent when event occured | [optional] 
**context_cross_app_correlation_id** | **str** | (optional) Cross application correlation ID | [optional] 
**context_device** | **str** | (optional) Device information | [optional] 
**context_app_sku** | **str** | (optional) Application SKU | [optional] 
**custom_properties** | [**CustomData**](CustomData.md) |  | [optional] 
**custom_segments** | [**CustomData**](CustomData.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



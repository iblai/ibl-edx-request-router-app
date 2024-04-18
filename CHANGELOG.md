# Changelog

## 0.4.0
* Makes `platform_key` a required JSON POST key to token proxy endpoint

## 0.3.0
* Add manager token proxy view

## 0.2.4
* Add verify toggle to manager proxy requests

## 0.2.3
GCP compatibility update
* Check for request body existence to avoid replicating empty body
* https://cloud.google.com/load-balancing/docs/https#illegal_request_and_response_handling

## 0.2.2
Allow additional characters in endpoint path regex

## 0.2.1
Add additional proxy request permission options
* Add settings to allow access to certain manager endpoints as unauthenticated and non-elevated users

## 0.2.0 - 21-06-17
Adds Koa compatibility
* Replaces `OAuth2Authentication` with `BearerAuthentication` when using Koa
* Maintains Ironwood compatibility

## 0.1.0 - Changelog created
Core version

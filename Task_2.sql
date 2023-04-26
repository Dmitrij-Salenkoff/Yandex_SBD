WITH r1 as (
    WITH request_sends as (
    select * from requests where type ='RequestSent'
    ), request_recieves as (
    select * from requests where type ='RequestReceived'
    )
    select extract(milliseconds from req.datetime - request_sends.datetime) as diff_request
    from request_sends
    join request_recieves req
    on request_sends.data=req.host and request_sends.request_id=req.parent_request_id
    ), r2 as (
    WITH response_sends as (
    select * from requests where type ='ResponseSent'
    ), response_recieves as (
    select * from requests where type ='ResponseReceived'
    )
    select extract(milliseconds
    from resp.datetime - response_sends.datetime) as diff_response
    from response_sends
    join response_recieves resp
    on response_sends.host=split_part(resp.data, E '\t', 1) and resp.request_id=response_sends.parent_request_id
    )
select sum(diff) / (select count(*)
                    from requests
                    where host = 'balancer.test.yandex.ru'
                      and parent_request_id is null
                      and type = 'RequestReceived') as avg_network_time_ms
from (select sum(diff_request) as diff
      from r1
      union
      select sum(diff_response) as diff
      from r2) as col

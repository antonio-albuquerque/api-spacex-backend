select
    latitude,
    longitude 
from starlink_tracking_history st 
where satelite_id = %satelite_id
    and creation_date <= %creation_date
    limit 1;

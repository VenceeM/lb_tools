QUERY = """
        select  
            bookings.created_at as "Booked At",
            bookings.must_start_at as "Appointment Date",
            customers.id as "Client ID",
            branches.name as "Branch Name",
            services.name as "Services",
            IFNULL(packages.name, ' ') as "Packages",
            case bookings.status WHEN 1 THEN "Pending" 
                    When 2 THEN "Ongoing"
                    When 3 THEN "Cancelled"
                    When 4 THEN "Finished"
                    When 5 THEN "Expired"
                    When 6 THEN "Voided"
                    else bookings.status end as "Status",
            branches.classification as "Classification"
            from bookings
            inner join booking_details on booking_details.booking_id = bookings.id
            inner join services on services.id = booking_details.service_id
            inner join customers on customers.id = bookings.customer_id 
            inner join branches on branches.id = bookings.branch_id
            left join packages on packages.id = booking_details.under_package_id
            where(bookings.must_start_at BETWEEN :start_date AND :end_date) and not (branches.id = 811) 
            order by customers.id asc, branches.name asc
        """
        
        
        

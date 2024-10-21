examples = [
    {
        "question": "What is the total spend for steel dynamic?",
        "query": "MATCH (s:Supplier {{supplier_name: 'Steel Dynamic'}})-[:SUPPLIES]->(po:PurchaseOrder) RETURN SUM(po.po_amount) AS TotalSpend",
    },
    {
        "question": "What is the total cost for all suppliers?",
        "query": "MATCH (s:Supplier)-[:SUPPLIES]->(po:PurchaseOrder) RETURN s.supplier_name AS Supplier, SUM(po.po_amount) AS TotalCost ORDER BY TotalCost DESC",
    },
    {
        "question": "Who are the top 5 suppliers with the highest supplier rating and their corresponding financial scores?",
        "query": "MATCH (s:Supplier) RETURN s.supplier_name AS Supplier, s.sustainability_score AS SupplierRating, s.financial_score AS FinancialScore ORDER BY s.sustainability_score DESC LIMIT 5",
    },
    {
        "question": "which suppliers have the highest financial score for Service and Product?",
        "query": "MATCH (s:Supplier)-[:OFFERS_SERVICE]->(c:Catalog) WITH DISTINCT s.supplier_name AS Supplier, s.financial_score AS FinancialScore, 'Service' AS Type ORDER BY FinancialScore DESC LIMIT 5 RETURN Supplier, FinancialScore, Type UNION ALL MATCH (s:Supplier)-[:OFFERS_PRODUCT]->(c:Catalog) WITH DISTINCT s.supplier_name AS Supplier, s.financial_score AS FinancialScore, 'Product' AS Type ORDER BY FinancialScore DESC LIMIT 5 RETURN Supplier, FinancialScore, Type",
    },
    {
        "question": "how many catogeries are there and which suppliers offers products and services in what categories",
        "query": "MATCH (c:Catalog) WITH c.supplier_name as supplier, c.category as category, c.parent_category as parent_category WHERE category IS NOT NULL WITH supplier, category, parent_category, COUNT(*) as offering_count WITH COUNT(DISTINCT category) as total_categories, COUNT(DISTINCT parent_category) as total_parent_categories, COLLECT(DISTINCT {{supplier: supplier, category: category, parent_category: parent_category, offering_count: offering_count}}) as supplier_category_details RETURN total_categories, total_parent_categories, supplier_category_details ORDER BY SIZE(supplier_category_details) DESC",
    },
    {
        "question": "Get more information about a Ground freight category",
        "query":"MATCH (c:Catalog) WHERE toLower(c.category) CONTAINS 'freight' OR toLower(c.parent_category) CONTAINS 'freight' OR toLower(c.service_name) CONTAINS 'freight' RETURN c.category, c.parent_category, c.service_name, c.equipment, c.route, c.base_rate_per_mile, c.fuel_surcharge, c.detention_rate_per_hour, c.liftgate_service_rate, c.additional_services, c.special_instructions, c.supplier_name, c.currency, c.lead_time, c.distance_miles LIMIT 10",

    },
    {
        "question": "How has my total procurement spend changed over the last 3 years?",
        "query":"MATCH (po:PurchaseOrder) WHERE po.po_date IS NOT NULL WITH datetime(po.po_date).year as year, sum(po.po_amount) as total_spend, count(po) as number_of_pos WITH collect({{year: year, total_spend: total_spend, number_of_pos: number_of_pos}}) as years_data UNWIND range(0, size(years_data)-2) as i WITH years_data[i] as current_year, years_data[i+1] as previous_year WITH current_year.year as year, current_year.total_spend as total_spend, current_year.number_of_pos as number_of_pos, CASE WHEN previous_year.total_spend > 0 THEN round(((current_year.total_spend - previous_year.total_spend) / previous_year.total_spend * 100.0), 2) ELSE null END as yoy_growth RETURN year, total_spend, number_of_pos, yoy_growth ORDER BY year DESC LIMIT 3;",

    },
    {
        "question": "How many POs are tied to contracts that are ending this year?",
        "query": "MATCH (po:PurchaseOrder)-[:SUPPLIES]-(s:Supplier)-[:HAS_CONTRACT]->(c:Contract) WHERE datetime(c.contract_end_date).year = datetime().year RETURN c.contract_id, c.supplier_name, c.category, datetime(c.contract_end_date) as end_date, COUNT(po) as number_of_pos, SUM(po.po_amount) as total_po_value ORDER BY end_date;",
    },
    {
        "question": "who is the cheapest supplier for Products?",
        "query": "MATCH (s:Supplier)-[o:OFFERS_PRODUCT]->(c:Catalog) WHERE c.unit_price IS NOT NULL WITH s, c, o, toFloat(c.unit_price) AS price ORDER BY price ASC WITH s, collect({{productName: c.product_name, price: price, poAmount: o.po_amount}})[0] AS cheapestProduct RETURN s.supplier_name AS supplier_name, cheapestProduct.productName AS product_name, cheapestProduct.price AS unit_price, s.sustainability_score AS sustainability_score, cheapestProduct.poAmount AS total_spend ORDER BY cheapestProduct.price ASC LIMIT 5",
    },
    {
        "question": "who is the cheapest supplier for Tranasport Services?",
        "query": "MATCH (s:Supplier)-[o:OFFERS_SERVICE]->(c:Catalog) WHERE c.base_rate_per_mile IS NOT NULL WITH s, c, o, toFloat(c.base_rate_per_mile) AS price ORDER BY price ASC WITH s, collect({{serviceName: c.service_name, price: price, poAmount: o.po_amount}})[0] AS cheapestService RETURN s.supplier_name AS supplier_name, cheapestService.serviceName AS service_name, cheapestService.price AS base_rate_per_mile, s.sustainability_score AS sustainability_score, cheapestService.poAmount AS total_spend ORDER BY cheapestService.price ASC LIMIT 5",
    },
    {
        "question": "whO is the cheapest supplier for Cloud migration?",
        "query": "MATCH (po:PurchaseOrder)-[:SUPPLIES]-(s:Supplier) WHERE ANY(keyword IN ['cloud migration', 'cloud', 'migration', 'cloud services'] WHERE toLower(po.category) CONTAINS toLower(keyword) OR toLower(po.parent_category) CONTAINS toLower(keyword)) WITH s, po.supplier_name as supplier_name, SUM(po.po_amount) as total_spend, COUNT(po) as order_count, AVG(po.financial_score) as financial_score, s.sustainability_score as sustainability_score RETURN supplier_name, round(total_spend / order_count, 2) as average_cost_per_order, order_count as number_of_orders, round(total_spend, 2) as total_spend, round(financial_score, 2) as financial_score, round(sustainability_score, 2) as sustainability_score ORDER BY average_cost_per_order ASC LIMIT 5;",
    },
    {
        "question": "What is the sum of TotalCost for all suppliers, along with the individual supplier costs?",
        "query": "MATCH (s:Supplier)-[:SUPPLIES]->(po:PurchaseOrder) WITH s.supplier_name AS Supplier, SUM(po.po_amount) AS SupplierTotalCost WITH COLLECT({{Supplier: Supplier, TotalCost: SupplierTotalCost}}) AS SupplierCosts, SUM(SupplierTotalCost) AS GrandTotal RETURN {{GrandTotal: GrandTotal, SupplierCosts: SupplierCosts}} AS Result",
    },
        {   "question":"Which contracts are expiring within the next 3 months?",
         "query":"MATCH (c:Contract) WHERE datetime(c.contract_end_date) >= datetime('2024-10-21T00:00:00') AND datetime(c.contract_end_date) <= datetime('2025-01-21T00:00:00') RETURN c.contract_id, c.supplier_name, c.category, c.contract_value, c.contract_end_date as expiry_date ORDER BY expiry_date ASC",

    },
    {   "question":"Which suppliers are offering the best payment terms (e.g., early payment discounts)?",
         "query":"MATCH (s:Supplier)-[:SUPPLIES]->(po:PurchaseOrder) WHERE po.payment_terms CONTAINS 'discount' RETURN DISTINCT s.supplier_name, po.payment_terms, s.financial_score, COUNT(po) as number_of_orders, ROUND(AVG(po.po_amount) * 100) / 100.0 as average_order_amount ORDER BY s.financial_score DESC",

    },
    {   "question":"for API Development and Integration Service What are the prices in 2024 and 2023?",
         "query":"MATCH (po:PurchaseOrder)-[:CREATED_ON]->(d:Date) WHERE po.parent_category = 'IT Professional Services' AND po.category = 'ITC-001-C: Software Development and Management' AND d.date.year IN [2023, 2024] RETURN d.date.year as Year, count(po) as Number_of_Orders, round(avg(po.fixed_cost), 2) as Average_Fixed_Cost, round(sum(po.po_amount), 2) as Total_Spend ORDER BY Year",

    },
    {   "question":"How many active contracts do I have with suppliers, and what is their total value?",
         "query":"MATCH (c:Contract) WHERE date(datetime(c.contract_end_date)) >= date() RETURN c.supplier_id AS supplier_id, c.supplier_name AS supplier_name, c.contract_id AS contract_id, c.contract_start_date AS contract_start_date, c.contract_end_date AS contract_end_date, c.contract_value AS contract_value ORDER BY c.contract_end_date DESC",

    },
    {   "question":"How many POs are tied to contracts that are ending this year?",
         "query":"MATCH (po:PurchaseOrder)-[:SUPPLIES]-(s:Supplier), (c:Contract) WHERE c.supplier_id = s.supplier_id AND datetime(c.contract_end_date).year = datetime().year RETURN c.contract_id, po.po_number, c.contract_start_date, c.contract_end_date ORDER BY c.contract_id, po.po_number",

    },
    ]

print(examples)
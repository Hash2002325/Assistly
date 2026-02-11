-- Mock data for Assistly

-- Insert plans
INSERT INTO plans VALUES 
('PLAN_BASIC', 'Basic Plan', 9.99, 'monthly', 'Email support, 5GB storage', TRUE),
('PLAN_PRO', 'Pro Plan', 29.99, 'monthly', '24/7 support, 50GB storage, Priority queue', TRUE),
('PLAN_ENTERPRISE', 'Enterprise Plan', 99.99, 'monthly', 'Dedicated support, Unlimited storage, Custom integrations', TRUE);

-- Insert customers
INSERT INTO customers VALUES 
('CUST001', 'John Doe', 'john.doe@email.com', '+1-555-0101', 'PLAN_PRO', NOW(), NOW()),
('CUST002', 'Jane Smith', 'jane.smith@email.com', '+1-555-0102', 'PLAN_BASIC', NOW(), NOW()),
('CUST003', 'Bob Johnson', 'bob.johnson@email.com', '+1-555-0103', 'PLAN_ENTERPRISE', NOW(), NOW()),
('CUST004', 'Alice Williams', 'alice.w@email.com', '+1-555-0104', 'PLAN_PRO', NOW(), NOW()),
('CUST005', 'Charlie Brown', 'charlie.b@email.com', '+1-555-0105', 'PLAN_BASIC', NOW(), NOW());

-- Insert billing history
INSERT INTO billing_history (customer_id, amount, billing_date, status, invoice_number, payment_method) VALUES
('CUST001', 29.99, '2024-01-15', 'paid', 'INV-001-202401', 'credit_card'),
('CUST001', 29.99, '2024-02-15', 'paid', 'INV-001-202402', 'credit_card'),
('CUST002', 9.99, '2024-01-20', 'paid', 'INV-002-202401', 'paypal'),
('CUST002', 9.99, '2024-02-20', 'failed', 'INV-002-202402', 'paypal'),
('CUST003', 99.99, '2024-01-10', 'paid', 'INV-003-202401', 'wire_transfer'),
('CUST004', 29.99, '2024-02-01', 'paid', 'INV-004-202402', 'credit_card'),
('CUST005', 9.99, '2024-02-05', 'pending', 'INV-005-202402', 'credit_card');

-- Insert support tickets
INSERT INTO tickets (customer_id, issue_type, subject, description, status, priority) VALUES
('CUST001', 'billing', 'Double charged', 'I was charged twice for my February subscription', 'open', 'high'),
('CUST002', 'technical', 'Cannot login', 'Getting error message when trying to access my account', 'in_progress', 'high'),
('CUST003', 'sales', 'Upgrade plan', 'Want to know about custom enterprise features', 'open', 'medium'),
('CUST004', 'technical', 'Slow performance', 'Dashboard is loading very slowly', 'resolved', 'low'),
('CUST005', 'billing', 'Payment failed', 'My payment method was declined', 'open', 'medium');
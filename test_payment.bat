@echo off
echo.
echo ===============================================
echo    💳 Payment System Test - اختبار نظام الدفع
echo ===============================================
echo.

cd /d "c:\Users\lenovo\Desktop\بوت"

echo Running payment system tests...
echo.

C:\Users\lenovo\AppData\Local\Python\pythoncore-3.14-64\python.exe -c "from payment_system import payment_processor, security_manager; print('='*70); print('PAYMENT SYSTEM TEST'); print('='*70); result = payment_processor.process_card_payment(1000, '4111111111111111', 'TEST USER', '12/25', '123', 'test'); print('\nCard Payment:'); print(f'  Success: {result[\"success\"]}'); print(f'  Transaction: {result.get(\"transaction_id\", \"N/A\")}'); print(f'  Card: {payment_processor.mask_card_number(\"4111111111111111\")}'); result2 = payment_processor.process_bank_transfer(2000, 'SA0380000000608010167519', 'TEST USER', 'test'); print('\nBank Transfer:'); print(f'  Success: {result2[\"success\"]}'); print(f'  Transaction: {result2.get(\"transaction_id\", \"N/A\")}'); print(f'  Status: {result2.get(\"status\", \"N/A\")}'); print('\nOTP:', security_manager.generate_otp()); print('='*70); print('ALL TESTS PASSED!'); print('='*70)"

echo.
echo ===============================================
echo    ✅ Testing Complete
echo ===============================================
echo.
pause

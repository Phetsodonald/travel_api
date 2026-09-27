from rest_framework import serializers
from .models import Budget,Expense

class BudgetSerializer(serializers.ModelSerializer):
    total_budget=serializers.ReadOnlyField()
    class Meta: 
        model=Budget; 
        fields='__all__'; 
        read_only_fields=['id','created_at','updated_at','total_budget']
    
    def validate(self,data):
        if any(v<0 for k,v in data.items() if k.endswith('_budget')): raise serializers.ValidationError('Budget values cannot be negative.')
        return data

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Expense; 
        fields='__all__'; 
        read_only_fields=['id','created_at','updated_at']
    
    def validate_amount(self,value):
        if value<=0: raise serializers.ValidationError('Expense must be greater than zero.')
        return value
    
    def validate(self,data):
        if data.get('amount') and data['amount']>1000000: raise serializers.ValidationError({'amount':'Expense is unusually large.'})
        return data

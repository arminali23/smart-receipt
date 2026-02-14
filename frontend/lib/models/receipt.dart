class ReceiptItem {
  final int id;
  final String productName;
  final double quantity;
  final double unitPrice;
  final double totalPrice;
  final String category;

  ReceiptItem({
    required this.id,
    required this.productName,
    required this.quantity,
    required this.unitPrice,
    required this.totalPrice,
    required this.category,
  });

  factory ReceiptItem.fromJson(Map<String, dynamic> json) {
    return ReceiptItem(
      id: json['id'],
      productName: json['product_name'],
      quantity: (json['quantity'] as num).toDouble(),
      unitPrice: (json['unit_price'] as num).toDouble(),
      totalPrice: (json['total_price'] as num).toDouble(),
      category: json['category'],
    );
  }
}

class Receipt {
  final int id;
  final String storeName;
  final double totalAmount;
  final DateTime createdAt;
  final List<ReceiptItem> items;

  Receipt({
    required this.id,
    required this.storeName,
    required this.totalAmount,
    required this.createdAt,
    required this.items,
  });

  factory Receipt.fromJson(Map<String, dynamic> json) {
    return Receipt(
      id: json['id'],
      storeName: json['store_name'],
      totalAmount: (json['total_amount'] as num).toDouble(),
      createdAt: DateTime.parse(json['created_at']),
      items: (json['items'] as List)
          .map((i) => ReceiptItem.fromJson(i))
          .toList(),
    );
  }
}

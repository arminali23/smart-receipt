import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/receipt.dart';

class ReceiptDetailScreen extends StatelessWidget {
  final Receipt receipt;

  const ReceiptDetailScreen({super.key, required this.receipt});

  Color _categoryColor(String category) {
    switch (category) {
      case 'Food & Groceries':
        return Colors.green;
      case 'Beverages':
        return Colors.blue;
      case 'Household':
        return Colors.orange;
      case 'Snacks':
        return Colors.purple;
      case 'Health & Beauty':
        return Colors.pink;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final dateFormat = DateFormat('EEEE, MMM dd, yyyy - HH:mm');

    return Scaffold(
      appBar: AppBar(
        title: Text(receipt.storeName),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Header card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Icon(Icons.store, size: 48, color: colorScheme.primary),
                  const SizedBox(height: 8),
                  Text(
                    receipt.storeName,
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  Text(
                    dateFormat.format(receipt.createdAt),
                    style: TextStyle(color: colorScheme.outline),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    '\$${receipt.totalAmount.toStringAsFixed(2)}',
                    style: TextStyle(
                      fontSize: 36,
                      fontWeight: FontWeight.bold,
                      color: colorScheme.primary,
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Items
          Text(
            'Items (${receipt.items.length})',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          ...receipt.items.map((item) => Card(
                child: ListTile(
                  title: Text(
                    item.productName,
                    style: const TextStyle(fontWeight: FontWeight.w500),
                  ),
                  subtitle: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: _categoryColor(item.category).withAlpha(30),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          item.category,
                          style: TextStyle(
                            fontSize: 11,
                            color: _categoryColor(item.category),
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        '${item.quantity.toStringAsFixed(item.quantity == item.quantity.roundToDouble() ? 0 : 1)} x \$${item.unitPrice.toStringAsFixed(2)}',
                        style: TextStyle(
                            color: colorScheme.outline, fontSize: 13),
                      ),
                    ],
                  ),
                  trailing: Text(
                    '\$${item.totalPrice.toStringAsFixed(2)}',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: colorScheme.primary,
                      fontSize: 16,
                    ),
                  ),
                ),
              )),
        ],
      ),
    );
  }
}

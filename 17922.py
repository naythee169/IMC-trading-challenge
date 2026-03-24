from datamodel import OrderDepth, TradingState, Order
from typing import List

class Trader:
    def run(self, state: TradingState):
        result = {}

        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []

            # 1. Position Management (CRITICAL: Limit is 20)
            current_pos = state.position.get(product, 0)
            LIMIT = 80

            # 2. Strategy for EMERALDS (Mean Reversion)
            if product == "EMERALDS":
                # found min spread was 8
                # the VWAP fair price was found to be 10000

                # Buy Order
                if current_pos < LIMIT:
                    buy_qty = LIMIT - current_pos
                    orders.append(Order(product, 9997, buy_qty))

                # Sell Order
                if current_pos > -LIMIT:
                    sell_qty = -LIMIT - current_pos
                    orders.append(Order(product, 10003, sell_qty))

            # 3. Strategy for TOMATOES (Dynamic Market Making)
            elif product == "TOMATOES":
                if len(order_depth.sell_orders) > 0 and len(order_depth.buy_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_bid = max(order_depth.buy_orders.keys())
                    mid_price = (best_ask + best_bid) / 2
                    delta = (best_ask - best_bid) / 4

                    buy_price = int(best_bid + 1)
                    sell_price = int(best_ask - 1)

                    if current_pos < LIMIT:
                        orders.append(Order(product, buy_price, LIMIT - current_pos))

                    if current_pos > -LIMIT:
                        orders.append(Order(product, sell_price, -LIMIT - current_pos))

            result[product] = orders

        traderData = ""
        conversions = 0
        return result, conversions, traderData
from portfolio.models import Holding


def get_net_worth() -> int:
    net_worth = sum([
        holding.total_value for holding in
        Holding.objects.only("id").all()
    ])
    return net_worth
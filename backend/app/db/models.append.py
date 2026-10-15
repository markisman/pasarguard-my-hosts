# APPEND this class to app/db/models.py (near the other models, e.g. after ProxyHost).


class AdminHostOverride(Base):
    """Per-admin customization of a host (name / order / visibility).

    Only affects the owning admin's own subscription output. Never changes the
    global host row.
    """

    __tablename__ = "admin_host_overrides"

    id: Mapped[int] = mapped_column(SqliteCompatibleBigInteger, primary_key=True, init=False, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(
        SqliteCompatibleBigInteger, ForeignKey("admins.id", ondelete="CASCADE"), index=True
    )
    host_id: Mapped[int] = mapped_column(
        SqliteCompatibleBigInteger, ForeignKey("hosts.id", ondelete="CASCADE"), index=True
    )
    # Custom remark; None => use the host's own remark
    display_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    # Custom order; None => use the host's own priority
    sort_order: Mapped[int | None] = mapped_column(nullable=True)
    # Hide this host from the admin's own subscriptions
    is_disabled: Mapped[bool] = mapped_column(default=False, server_default="0")

    __table_args__ = (UniqueConstraint("admin_id", "host_id", name="uix_admin_host_override"),)

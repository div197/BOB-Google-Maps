"""bob_core.health_cli

Health check CLI commands for BOB Google Maps.
"""
import json
import click
from .health_check import get_health_monitor, setup_default_health_checks
from .circuit_breaker import get_all_circuit_breakers
from .error_codes import get_error_manager


@click.group()
def health():
    """Health monitoring and diagnostics commands."""
    pass


@health.command()
@click.option('--format', 'output_format', default='json', 
              type=click.Choice(['json', 'table']),
              help='Output format')
def status(output_format):
    """Check overall system health status."""
    monitor = setup_default_health_checks()
    
    # Run all health checks
    results = monitor.run_all_checks()
    summary = monitor.get_health_summary()
    
    if output_format == 'json':
        click.echo(json.dumps(summary, indent=2))
    else:
        # Table format
        click.echo(f"🏥 BOB Google Maps Health Status")
        click.echo(f"{'='*50}")
        click.echo(f"Overall Status: {summary['overall_status'].upper()}")
        click.echo(f"Timestamp: {summary['timestamp']}")
        click.echo(f"Total Checks: {summary['statistics']['total_checks']}")
        click.echo()
        
        for name, result in summary['checks'].items():
            status_emoji = {
                'healthy': '✅',
                'warning': '⚠️',
                'critical': '❌',
                'unknown': '❓'
            }.get(result['status'], '❓')
            
            click.echo(f"{status_emoji} {name}: {result['status']} ({result['duration_ms']:.1f}ms)")
            if result['status'] != 'healthy':
                click.echo(f"   Message: {result['message']}")


@health.command()
def circuits():
    """Show circuit breaker status."""
    breakers = get_all_circuit_breakers()
    
    if not breakers:
        click.echo("No circuit breakers registered.")
        return
    
    click.echo("🔌 Circuit Breaker Status")
    click.echo("=" * 50)
    
    for name, breaker in breakers.items():
        metrics = breaker.get_metrics()
        state_emoji = {
            'closed': '🟢',
            'open': '🔴',
            'half_open': '🟡'
        }.get(metrics['state'], '❓')
        
        click.echo(f"{state_emoji} {name}: {metrics['state'].upper()}")
        click.echo(f"   Requests: {metrics['total_requests']} "
                  f"(Success: {metrics['successful_requests']}, "
                  f"Failed: {metrics['failed_requests']})")
        click.echo(f"   Success Rate: {metrics['success_rate']:.1%}")
        if metrics['circuit_open_count'] > 0:
            click.echo(f"   Times Opened: {metrics['circuit_open_count']}")


@health.command()
def errors():
    """Show error statistics."""
    error_manager = get_error_manager()
    stats = error_manager.get_error_statistics()
    
    click.echo("🚨 Error Statistics")
    click.echo("=" * 50)
    click.echo(f"Total Errors: {stats['total_errors']}")
    
    if stats['total_errors'] == 0:
        click.echo("✅ No errors recorded!")
        return
    
    click.echo("\nTop Errors:")
    for error in stats['top_errors'][:5]:
        click.echo(f"  {error['error_code']}: {error['count']} occurrences")
    
    click.echo("\nBy Category:")
    for category, data in stats['categories'].items():
        click.echo(f"  {category}: {data['count']} errors")
    
    if stats['recovery_rates']:
        click.echo("\nRecovery Rates:")
        for category, rate in stats['recovery_rates'].items():
            click.echo(f"  {category}: {rate:.1%}")


@health.command()
@click.option('--interval', default=60, help='Check interval in seconds')
@click.option('--duration', default=300, help='Monitoring duration in seconds')
def monitor(interval, duration):
    """Start continuous health monitoring."""
    import time
    
    monitor = setup_default_health_checks()
    monitor.check_interval = interval
    
    click.echo(f"🔍 Starting health monitoring (interval: {interval}s, duration: {duration}s)")
    click.echo("Press Ctrl+C to stop early")
    
    monitor.start_monitoring()
    
    try:
        start_time = time.time()
        while time.time() - start_time < duration:
            time.sleep(5)  # Check every 5 seconds if we should stop
            
            # Show brief status update
            summary = monitor.get_health_summary()
            status = summary['overall_status']
            timestamp = summary['timestamp'].split('T')[1][:8]  # Just time
            
            click.echo(f"[{timestamp}] Status: {status.upper()}", nl=False)
            
            # Show any critical issues
            critical_count = summary['statistics']['critical']
            if critical_count > 0:
                click.echo(f" - {critical_count} CRITICAL issues!", fg='red')
            else:
                click.echo(" - All systems healthy", fg='green')
                
    except KeyboardInterrupt:
        click.echo("\n⏹️  Monitoring stopped by user")
    finally:
        monitor.stop_monitoring()
        click.echo("✅ Health monitoring stopped")


if __name__ == '__main__':
    health() 
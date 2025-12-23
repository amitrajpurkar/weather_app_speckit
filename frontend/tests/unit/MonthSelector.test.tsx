import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import MonthSelector from '../../components/MonthSelector';


describe('MonthSelector', () => {
  it('renders options for available months and calls onChange', async () => {
    const user = userEvent.setup();
    const onChange = jest.fn();

    render(
      <MonthSelector availableMonths={[1, 3]} selectedMonth={null} onChange={onChange} />
    );

    expect(screen.getByLabelText(/select month/i)).toBeInTheDocument();

    await user.selectOptions(screen.getByRole('combobox'), '3');
    expect(onChange).toHaveBeenCalledWith(3);
  });

  it('disables selector when there are no available months', () => {
    const onChange = jest.fn();

    render(<MonthSelector availableMonths={[]} selectedMonth={null} onChange={onChange} />);

    expect(screen.getByRole('combobox')).toBeDisabled();
    expect(screen.getByText(/no months with data/i)).toBeInTheDocument();
  });
});

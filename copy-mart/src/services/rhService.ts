import api from '@/config/api';

// Employees
export interface Employee {
  employee_id: number;
  user_id: number;
  nss: string;
  rfc: string;
  curp: string;
  birthday: string;
  hire_date: string;
  phone_emergency: string;
  contact_emergency: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface EmployeeCreate {
  user_id: number;
  nss: string;
  rfc: string;
  curp: string;
  birthday: string;
  hire_date: string;
  phone_emergency: string;
  contact_emergency: string;
}

export interface EmployeeUpdate {
  nss?: string;
  rfc?: string;
  curp?: string;
  birthday?: string;
  hire_date?: string;
  phone_emergency?: string;
  contact_emergency?: string;
  is_active?: boolean;
}

// Payrolls
export interface Payroll {
  payroll_id: number;
  employee_id: number;
  salary: number;
  pay_day: string;
  bonus: number;
  commission: number;
  status: 'PENDIENTE' | 'APROBADO' | 'RECHAZADO' | 'ACTIVO' | 'PAGADO';
  created_at: string;
  updated_at: string;
}

export interface PayrollCreate {
  employee_id: number;
  salary: number;
  pay_day: string;
  bonus?: number;
  commission?: number;
}

export interface PayrollUpdate {
  salary?: number;
  pay_day?: string;
  bonus?: number;
  commission?: number;
  status?: 'PENDIENTE' | 'APROBADO' | 'RECHAZADO' | 'ACTIVO' | 'PAGADO';
}

// Vacations
export interface Vacation {
  vacation_id: number;
  employee_id: number;
  vacation_days: number;
  start_date: string;
  end_date: string;
  notes?: string;
  status: 'PENDIENTE' | 'APROBADO' | 'RECHAZADO';
  requested_by: number;
  created_at: string;
  updated_at: string;
}

export interface VacationCreate {
  employee_id: number;
  vacation_days: number;
  start_date: string;
  end_date: string;
  notes?: string;
  requested_by: number;
}

export interface VacationUpdate {
  vacation_days?: number;
  start_date?: string;
  end_date?: string;
  status?: 'PENDIENTE' | 'APROBADO' | 'RECHAZADO';
}

// Administrative Records
export interface AdministrativeRecord {
  record_id: number;
  employee_id: number;
  type: 'RETROALIMENTACION_ESCRITA' | 'AMONESTACION' | 'ACTA_ADMINISTRATIVA' | 'ENTREVISTA_AUSENTISMO';
  issue_date: string;
  description: string;
  issued_by: number;
  created_at: string;
  updated_at: string;
}

export interface AdministrativeRecordCreate {
  employee_id: number;
  type: 'RETROALIMENTACION_ESCRITA' | 'AMONESTACION' | 'ACTA_ADMINISTRATIVA' | 'ENTREVISTA_AUSENTISMO';
  issue_date: string;
  description: string;
  issued_by: number;
}

export interface AdministrativeRecordUpdate {
  type?: 'RETROALIMENTACION_ESCRITA' | 'AMONESTACION' | 'ACTA_ADMINISTRATIVA' | 'ENTREVISTA_AUSENTISMO';
  issue_date?: string;
  description?: string;
}

// Absences
export interface Absence {
  absence_id: number;
  employee_id: number;
  absence_type: 'ENFERMEDAD' | 'AUSENTISMO' | 'PERMISO_PERSONAL' | 'OTRO';
  start_date: string;
  end_date: string;
  is_justified: boolean;
  justification?: string;
  file_path?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface AbsenceCreate {
  employee_id: number;
  absence_type: 'ENFERMEDAD' | 'AUSENTISMO' | 'PERMISO_PERSONAL' | 'OTRO';
  start_date: string;
  end_date: string;
  is_justified?: boolean;
  justification?: string;
  file_path?: string;
  notes?: string;
}

export interface AbsenceUpdate {
  absence_type?: 'ENFERMEDAD' | 'AUSENTISMO' | 'PERMISO_PERSONAL' | 'OTRO';
  start_date?: string;
  end_date?: string;
  is_justified?: boolean;
  justification?: string;
  file_path?: string;
  notes?: string;
}

const rhService = {
  // Employees
  employees: {
    async create(data: EmployeeCreate): Promise<Employee> {
      const response = await api.post('/rh/employees', data);
      return response.data;
    },

    async getAll(params?: { is_active?: boolean }): Promise<Employee[]> {
      const response = await api.get('/rh/employees', { params });
      return response.data;
    },

    async getById(employeeId: number): Promise<Employee> {
      const response = await api.get(`/rh/employees/${employeeId}`);
      return response.data;
    },

    async getByUserId(userId: number): Promise<Employee> {
      const response = await api.get(`/rh/employees/user/${userId}`);
      return response.data;
    },

    async update(employeeId: number, data: EmployeeUpdate): Promise<Employee> {
      const response = await api.put(`/rh/employees/${employeeId}`, data);
      return response.data;
    },

    async delete(employeeId: number): Promise<void> {
      await api.delete(`/rh/employees/${employeeId}`);
    },

    async getSummary(employeeId: number): Promise<any> {
      const response = await api.get(`/rh/employees/${employeeId}/summary`);
      return response.data;
    }
  },

  // Payrolls
  payrolls: {
    async create(data: PayrollCreate): Promise<Payroll> {
      const response = await api.post('/rh/payrolls', data);
      return response.data;
    },

    async getById(payrollId: number): Promise<Payroll> {
      const response = await api.get(`/rh/payrolls/${payrollId}`);
      return response.data;
    },

    async getByEmployee(employeeId: number): Promise<Payroll[]> {
      const response = await api.get(`/rh/employees/${employeeId}/payrolls`);
      return response.data;
    },

    async update(payrollId: number, data: PayrollUpdate): Promise<Payroll> {
      const response = await api.put(`/rh/payrolls/${payrollId}`, data);
      return response.data;
    }
  },

  // Vacations
  vacations: {
    async create(data: VacationCreate): Promise<Vacation> {
      const response = await api.post('/rh/vacations', data);
      return response.data;
    },

    async getById(vacationId: number): Promise<Vacation> {
      const response = await api.get(`/rh/vacations/${vacationId}`);
      return response.data;
    },

    async getByEmployee(employeeId: number): Promise<Vacation[]> {
      const response = await api.get(`/rh/employees/${employeeId}/vacations`);
      return response.data;
    },

    async getVacationDays(employeeId: number): Promise<any> {
      const response = await api.get(`/rh/employees/${employeeId}/vacation-days`);
      return response.data;
    },

    async update(vacationId: number, data: VacationUpdate): Promise<Vacation> {
      const response = await api.put(`/rh/vacations/${vacationId}`, data);
      return response.data;
    }
  },

  // Administrative Records
  administrativeRecords: {
    async create(data: AdministrativeRecordCreate): Promise<AdministrativeRecord> {
      const response = await api.post('/rh/administrative-records', data);
      return response.data;
    },

    async getById(recordId: number): Promise<AdministrativeRecord> {
      const response = await api.get(`/rh/administrative-records/${recordId}`);
      return response.data;
    },

    async getByEmployee(employeeId: number): Promise<AdministrativeRecord[]> {
      const response = await api.get(`/rh/employees/${employeeId}/administrative-records`);
      return response.data;
    },

    async update(recordId: number, data: AdministrativeRecordUpdate): Promise<AdministrativeRecord> {
      const response = await api.put(`/rh/administrative-records/${recordId}`, data);
      return response.data;
    }
  },

  // Absences
  absences: {
    async create(data: AbsenceCreate): Promise<Absence> {
      const response = await api.post('/rh/absences', data);
      return response.data;
    },

    async getById(absenceId: number): Promise<Absence> {
      const response = await api.get(`/rh/absences/${absenceId}`);
      return response.data;
    },

    async getByEmployee(employeeId: number, params?: {
      start_date?: string;
      end_date?: string;
      absence_type?: string;
    }): Promise<Absence[]> {
      const response = await api.get(`/rh/employees/${employeeId}/absences`, { params });
      return response.data;
    },

    async getByDateRange(employeeId: number, startDate: string, endDate: string): Promise<Absence[]> {
      const response = await api.get(`/rh/employees/${employeeId}/absences/range`, {
        params: { start_date: startDate, end_date: endDate }
      });
      return response.data;
    },

    async update(absenceId: number, data: AbsenceUpdate): Promise<Absence> {
      const response = await api.put(`/rh/absences/${absenceId}`, data);
      return response.data;
    }
  },

  // Stats
  async getDepartmentStats(department: string): Promise<any> {
    const response = await api.get(`/rh/stats/department/${department}`);
    return response.data;
  }
};

export default rhService;
